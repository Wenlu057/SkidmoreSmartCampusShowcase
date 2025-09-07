from __future__ import annotations
import time
from typing import Callable, List

def time_algorithm(alg: Callable, data: List, repeats: int = 3):
    elapsed = []
    for _ in range(repeats):
        a = data[:]
        t0 = time.perf_counter()
        alg(a)
        elapsed.append(time.perf_counter() - t0)
    return sum(elapsed)/len(elapsed)
