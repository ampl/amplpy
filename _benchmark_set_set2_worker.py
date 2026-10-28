#!/usr/bin/env python
"""Worker: benchmark one set_data path at one row count (2-arity set).
Prints: wall_ms cpu_ms
"""
import gc
import sys
import time
import numpy as np
import pandas as pd

path, N, ampl_dir = sys.argv[1], int(sys.argv[2]), sys.argv[3]

import amplpy
amplpy.add_to_path(ampl_dir)

MODEL = "set PAIRS dimen 2;\n"

k = np.arange(N)
side = int(np.ceil(np.sqrt(N)))
df = pd.DataFrame(
    index=pd.MultiIndex.from_arrays([k // side, k % side], names=["i", "j"])
)

if path == "dataframe":
    def do_set(a): a.set_data_df(df, "PAIRS")
else:
    def do_set(a): a.set_data(df, "PAIRS")


def measure_one():
    a = amplpy.AMPL()
    a.eval(MODEL)
    gc.collect()

    t0_wall = time.perf_counter()
    t0_cpu  = time.process_time()
    do_set(a)
    elapsed_wall = time.perf_counter() - t0_wall
    elapsed_cpu  = time.process_time() - t0_cpu

    a.close()
    return elapsed_wall * 1000, elapsed_cpu * 1000


wall_ms, cpu_ms = measure_one()
print(f"{wall_ms} {cpu_ms}")
