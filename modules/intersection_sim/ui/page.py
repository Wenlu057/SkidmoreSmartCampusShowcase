from __future__ import annotations
import streamlit as st
import pandas as pd
from pathlib import Path
from ..ds.simulator import IntersectionSim, SimParams

DATA = Path(__file__).parents[1] / "data"

def meta():
    return {
        "title": "Smart Intersection Simulator (Skidmore Campus Gate)",
        "description": "Simulate a 4-way signal at North Broadway @ Skidmore Campus Gate with DS-only queues and event scheduling.",
    }

def load_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / name)

def render():
    st.write("""This simulator focuses on **North Broadway @ Campus Gate** (near Case Center).
Use your own 5‑minute arrival counts by replacing the CSVs in `modules/intersection_sim/data/`.


Each approach uses a FIFO **Queue**; a custom **PriorityQueue** orders arrivals, phase changes, and fixed‑headway service slots..
""")

    scenario = st.selectbox("Arrival scenario (5‑min bins)", ["arrivals_weekday_midday.csv", "arrivals_rush_pm.csv"])
    df = load_csv(scenario)
    st.caption("First 5 bins of arrivals (vehicles per 5‑min)")
    st.dataframe(df.head(), hide_index=True)

    st.sidebar.header("Signal parameters")
    duration = st.sidebar.slider("Duration (minutes)", 15, 180, 60, step=5)
    ns_green = st.sidebar.slider("NS green (s)", 10, 120, 30, step=5)
    ew_green = st.sidebar.slider("EW green (s)", 10, 120, 30, step=5)
    headway = st.sidebar.slider("Service headway (s)", 1.0, 5.0, 2.0, step=0.5)
    seed = st.sidebar.number_input("Random seed", min_value=0, max_value=10000, value=42, step=1)

    if st.button("Run simulation", type="primary"):
        P = SimParams(duration_min=duration, ns_green_s=ns_green, ew_green_s=ew_green, headway_s=headway, seed=int(seed))
        sim = IntersectionSim(P, df)
        res = sim.run()

        st.subheader("Metrics")
        m = res.metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Total served", m["served_total"])
        c2.metric("Max queue N/S/E/W", f"{m['max_q_N']}/{m['max_q_S']}/{m['max_q_E']}/{m['max_q_W']}")
        c3.metric("Avg delay (s) N/S/E/W", f"{m['avg_delay_N_s']}/{m['avg_delay_S_s']}/{m['avg_delay_E_s']}/{m['avg_delay_W_s']}")

        st.write(pd.DataFrame([m]))

        st.subheader("Queue length over time (events)")
        ts = res.timeseries.set_index("t")[['N','S','E','W']]
        st.line_chart(ts)

        st.info("Try different green splits to see impact on queues and delays. Students can extend with pedestrian phases and emergency preemption.")
    else:
        st.info("Adjust parameters and click **Run simulation**.")
