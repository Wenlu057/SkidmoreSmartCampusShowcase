# Smart Intersection Simulator — Skidmore (Campus Gate)
A **discrete‑event, data‑structures‑first** simulator of a single 4‑way intersection tailored to **Skidmore College**.

**Intersection default:** *North Broadway @ Campus Gate* (near Case Center).  
Use your own counts by replacing CSVs in `data/`.

## What this module demonstrates
- `Queue` for each approach (N/S/E/W) — vehicles line up FCFS.
- `PriorityQueue<Event>` for the global simulation clock.
- **Metrics:** average delay, throughput, max queue per approach, queue‑length time series.
