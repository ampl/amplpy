import polars as pl
import amplpy
import time


pdf = pl.DataFrame({
    "Column2": [i * 2 for i in range(1_000_001)]
})


def nanoarrow_function():
   ampl = amplpy.AMPL()
   ampl.eval("param p{0..1000000} default 1;")
   p = ampl.getParameter("p")
   t0 = time.perf_counter()
   p.set_values(pdf)
   t1 = time.perf_counter()
   elapsed_wall = t1 - t0
   print(f"Wall Time (perf):  {elapsed_wall:.6f} seconds")

#def beta_function():
#   ampl = amplpy.AMPL()
#   ampl.eval("param p{0..1000000} default 1;")
#   p = ampl.getParameter("p")
#   t0 = time.perf_counter()
#   p.setValues(pdf)
#   t1 = time.perf_counter()
#   elapsed_wall = t1 - t0
#   df = ampl.get_data_arrow("p")
#   print(df)
#   print(f"Wall Time (perf):  {elapsed_wall:.6f} seconds")

def main():
   nanoarrow_function()
   #beta_function()

main()
