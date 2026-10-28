#!/usr/bin/env python
"""
Scaling benchmark: get_data DataFrame vs Arrow
Data is pre-loaded before each timed run.
Each (path, N) runs in its own subprocess for a clean baseline.
Best run selected by CPU time.
"""
import subprocess
import sys
import os

SIZES    = [1_000, 10_000, 100_000, 500_000, 1_000_000, 5_000_000, 10_000_000]
REPS     = 3
NCOLS    = 3
AMPL_DIR = "/home/lentz/Developer/ampl.linux-intel64"

_WORKER = os.path.join(os.path.dirname(__file__), "_benchmark_get_worker.py")


def run_once(path, n):
    result = subprocess.run(
        [sys.executable, _WORKER, path, str(n), str(NCOLS), AMPL_DIR],
        capture_output=True, text=True, check=True,
    )
    return tuple(map(float, result.stdout.strip().split()))


def run(path, n):
    results = [run_once(path, n) for _ in range(REPS)]
    return min(results, key=lambda r: r[1])   # best by CPU time


def fmt_n(n):
    if n >= 1_000_000: return f"{n // 1_000_000}M"
    if n >= 1_000:     return f"{n // 1_000}k"
    return str(n)

def fmt_ms(ms):
    return f"{ms / 1000:.2f}s" if ms >= 1000 else f"{ms:.1f}ms"


print(f"\nScaling benchmark: get_data  ({NCOLS} float64 cols, best of {REPS} runs)\n")
print(f"{'':>6s}  {'--- DataFrame ---':^17s}  {'--- Arrow ---':^17s}  {'factors':^15s}")
print(f"{'rows':>6s}  {'wall':>7s} {'cpu':>7s}  {'wall':>7s} {'cpu':>7s}  {'wall':>7s} {'cpu':>7s}")
SEP = "-" * 66
print(SEP)

for n in SIZES:
    df_wall, df_cpu = run("dataframe", n)
    ar_wall, ar_cpu = run("arrow",     n)

    print(
        f"{fmt_n(n):>6s}  "
        f"{fmt_ms(df_wall):>7s} {fmt_ms(df_cpu):>7s}  "
        f"{fmt_ms(ar_wall):>7s} {fmt_ms(ar_cpu):>7s}  "
        f"{df_wall / ar_wall:>6.2f}x {df_cpu / ar_cpu:>6.2f}x"
    )

print(SEP)
print()
