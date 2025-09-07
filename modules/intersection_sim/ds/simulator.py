from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple
import numpy as np
import pandas as pd
from .queue import Queue
from .heap import MinHeap

@dataclass(order=True)
class Event:
    t: float
    seq: int
    kind: str
    payload: tuple

class EventPQ:
    def __init__(self):
        self.h = MinHeap()
    def push(self, e: Event):
        self.h.push((e.t, e.seq, e.kind, e.payload))
    def pop(self) -> Event:
        t, seq, kind, payload = self.h.pop()
        return Event(t, seq, kind, payload)
    def __len__(self): return len(self.h)

@dataclass
class SimParams:
    duration_min: int = 60
    ns_green_s: float = 30.0
    ew_green_s: float = 30.0
    headway_s: float = 2.0
    seed: int = 42

@dataclass
class SimResult:
    metrics: Dict[str, float]
    timeseries: pd.DataFrame

class IntersectionSim:
    def __init__(self, params: SimParams, arrivals_df: pd.DataFrame):
        self.P = params
        self.arrivals_df = arrivals_df.copy()
        self.queues = {d: Queue() for d in ["N","S","E","W"]}
        self.arrival_time: Dict[str, Queue] = {d: Queue() for d in ["N","S","E","W"]}
        self.phase = "NS"
        self.seq = 0
        self.now = 0.0
        self.served = {d: 0 for d in ["N","S","E","W"]}
        self.total_delay = {d: 0.0 for d in ["N","S","E","W"]}
        self.max_q = {d: 0 for d in ["N","S","E","W"]}
        self.times = []

    def _ev(self, t, kind, payload=()):
        self.seq += 1
        return Event(t, self.seq, kind, payload)

    def _record(self):
        self.times.append({
            "t": self.now,
            **{d: len(self.queues[d]) for d in ["N","S","E","W"]}
        })
        for d in ["N","S","E","W"]:
            self.max_q[d] = max(self.max_q[d], len(self.queues[d]))

    def _load_arrivals(self) -> List[Tuple[float, str]]:
        rng = np.random.default_rng(self.P.seed)
        arrivals: List[Tuple[float, str]] = []
        for _, row in self.arrivals_df.iterrows():
            t0 = float(row["bin_start_min"]) * 60.0
            t1 = t0 + 5*60.0
            for d in ["N","S","E","W"]:
                c = int(row[d])
                if c <= 0: continue
                times = t0 + rng.random(c) * (t1 - t0)
                arrivals.extend([(float(t), d) for t in times])
        arrivals = [(t, d) for (t,d) in arrivals if t <= self.P.duration_min * 60.0]
        arrivals.sort(key=lambda x: x[0])
        return arrivals

    def _gen_phase_events(self) -> List[Event]:
        t = 0.0
        evs = []
        ns, ew = self.P.ns_green_s, self.P.ew_green_s
        phase = "NS"
        while t <= self.P.duration_min * 60.0 + 1e-6:
            evs.append(self._ev(t, "PHASE", (phase,)))
            head = self.P.headway_s
            k = 0
            while t + k*head < t + (ns if phase == "NS" else ew) - 1e-9:
                evs.append(self._ev(t + k*head, "SERVICE", (phase,)))
                k += 1
            t += ns if phase == "NS" else ew
            phase = "EW" if phase == "NS" else "NS"
        return evs

    def run(self) -> SimResult:
        pq = EventPQ()
        for (t, d) in self._load_arrivals():
            pq.push(self._ev(t, "ARRIVAL", (d,)))
        for e in self._gen_phase_events():
            pq.push(e)

        rr = {"NS": 0, "EW": 0}
        order = {"NS": ["N","S"], "EW": ["E","W"]}

        while len(pq):
            ev = pq.pop()
            self.now = ev.t
            if self.now > self.P.duration_min * 60.0 + 1e-9:
                break
            if ev.kind == "PHASE":
                (phase,) = ev.payload
                self.phase = phase
                self._record()
            elif ev.kind == "ARRIVAL":
                (d,) = ev.payload
                self.queues[d].enqueue(1)
                self.arrival_time[d].enqueue(self.now)
                self._record()
            elif ev.kind == "SERVICE":
                (phase,) = ev.payload
                dirs = order[phase]
                i = rr[phase]
                for j in range(2):
                    d = dirs[(i + j) % 2]
                    if not self.queues[d].is_empty():
                        self.queues[d].dequeue()
                        t_arr = self.arrival_time[d].dequeue()
                        self.served[d] += 1
                        self.total_delay[d] += (self.now - t_arr)
                        rr[phase] = (dirs.index(d) + 1) % 2
                        break
                self._record()

        tot_served = sum(self.served.values())
        avg_delay = {d: (self.total_delay[d]/self.served[d] if self.served[d] else 0.0) for d in ["N","S","E","W"]}
        metrics = {
            "duration_min": self.P.duration_min,
            "ns_green_s": self.P.ns_green_s,
            "ew_green_s": self.P.ew_green_s,
            "headway_s": self.P.headway_s,
            "served_total": tot_served,
            **{f"served_{d}": self.served[d] for d in ["N","S","E","W"]},
            **{f"avg_delay_{d}_s": round(avg_delay[d], 2) for d in ["N","S","E","W"]},
            **{f"max_q_{d}": self.max_q[d] for d in ["N","S","E","W"]},
        }
        ts = pd.DataFrame(self.times).sort_values("t")
        return SimResult(metrics=metrics, timeseries=ts)
