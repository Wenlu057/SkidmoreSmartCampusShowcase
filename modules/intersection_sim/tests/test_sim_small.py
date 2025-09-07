from ..ds.simulator import IntersectionSim, SimParams
import pandas as pd

def test_single_arrival_served():
    df = pd.DataFrame([{"bin_start_min": 0, "N": 1, "S": 0, "E": 0, "W": 0}])
    P = SimParams(duration_min=5, ns_green_s=30.0, ew_green_s=30.0, headway_s=2.0, seed=0)
    sim = IntersectionSim(P, df)
    res = sim.run()
    assert res.metrics["served_N"] == 1
    assert res.metrics["served_total"] == 1
