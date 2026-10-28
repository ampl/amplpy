#!/usr/bin/env python
"""Worker: benchmark one set_data path at one row count.
Prints: wall_ms cpu_ms
"""
import gc
import sys
import time
import numpy as np
import pandas as pd

path, N, NCOLS, ampl_dir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]

import amplpy
amplpy.add_to_path(ampl_dir)

col_defs = "\n".join(f"param val{i+1}{{S}};" for i in range(NCOLS))
MODEL    = f"set S;\n{col_defs}\n"

rng = np.random.default_rng(42)
df  = pd.DataFrame(
    {f"val{i+1}": rng.random(N) for i in range(NCOLS)},
    index=pd.Index(np.arange(N), name="S"),
)

if path == "dataframe":
    def do_set(a): a.set_data_df(df, "S")
else:
    def do_set(a): a.set_data(df, "S")


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
