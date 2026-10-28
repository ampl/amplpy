#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import itertools
import string
import random
import os
from amplpy import DataFrameArrow
from . import TestBase

try:
    import pyarrow as pa
except ImportError:
    pa = None
try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import nanoarrow as na
except ImportError:
    na = None

class TestDataFrameArrow(TestBase.TestBase):
    """Test DataFrame."""

    def test_pandas_arrow(self):
        ampl = self.ampl
        if pd is None:
            self.skipTest("pandas not available")
        if pa is None:
            self.skipTest("pyarrow not available")
        if na is None:
            self.skipTest("nanoarrow not available")
        df = pd.DataFrame({"a": [1, 2], "b": [3.5, 4]}, index=["x", "y"])
        ampl.eval(
            """
            set S;
            param a{S};
            param b{S};
        """
        )
        ampl.set_data(df, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["x", "y"])
        self.assertEqual(ampl.param["a"].num_instances(), 2)
        self.assertEqual(ampl.param["a"]["x"], 1)
        self.assertEqual(ampl.param["a"]["y"], 2)
        self.assertEqual(ampl.param["b"].num_instances(), 2)
        self.assertEqual(ampl.param["b"]["x"], 3.5)
        self.assertEqual(ampl.param["b"]["y"], 4)

    def test_pandas_arrow2(self):
        ampl = self.ampl
        #if pd is None:
        #    self.skipTest("pandas not available")
        #if pa is None:
        #    self.skipTest("pyarrow not available")
        #if na is None:
        #    self.skipTest("nanoarrow not available")
        df = pd.DataFrame({"a": [1, 2], "b": [3.5, 4]}, index=["x", "y"])
        ampl.eval(
            """
            set S;
            param a{S};
            param b{S};
        """
        )
        ampl.set_data(df, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["x", "y"])
        self.assertEqual(ampl.param["a"]["x"], 1)
        self.assertEqual(ampl.param["a"]["y"], 2)
        self.assertEqual(ampl.param["b"]["x"], 3.5)
        self.assertEqual(ampl.param["b"]["y"], 4)

        ampl.eval("reset data;")
        df2 = pd.DataFrame(
            {
                "a": [10, 20, 30],
            },
            index=["x", "y", "z"],
        )
        ampl.set_data(df2, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["x", "y", "z"])
        self.assertEqual(ampl.param["a"]["x"], 10)
        self.assertEqual(ampl.param["a"]["y"], 20)
        self.assertEqual(ampl.param["a"]["z"], 30)
        
        
        ampl.eval("reset data;")
        df3 = pd.DataFrame({}, index=["xx", "yy"])
        ampl.set_data(df3, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["xx", "yy"])

        csv_file = os.path.join(os.path.dirname(__file__), "data.csv")
        p_df = pd.read_csv(csv_file, sep=";", index_col=0)
        #df = DataFrame.from_pandas(p_df)
        #self.assertTrue(isinstance(df.to_dict(), dict))
        #self.assertEqual(set(df.to_dict().keys()), set([1.0, 2.0, 3.0]))
        #self.assertEqual(set(df.to_list()[0]), set([1.0, 0.01]))
        #self.assertEqual(set(df.to_list()[1]), set([2.0, 0.02]))
        #self.assertEqual(set(df.to_list()[2]), set([3.0, 0.03]))

    def test_setindex(self):
        ampl = self.ampl
        ampl.eval(
            """
            set NUTR;
            param n_min {NUTR} >= 0;
            param n_max {i in NUTR} >= n_min[i];
            """
            )
        nutr_df = pd.DataFrame(
            [
                ("A", 700, 20000),
                ("C", 500, 3000),
                ("B1", 100, 777),
                ("B2", 60, 500)
            ],
            columns=["NUTR", "n_min", "n_max"],
        ).set_index("NUTR")
        ampl.set_data(nutr_df, "NUTR")
        self.assertEqual(list(ampl.set["NUTR"].members()), ["A", "C", "B1", "B2"])
        self.assertEqual(ampl.param["n_min"]["A"], 700)
        self.assertEqual(ampl.param["n_min"]["C"], 500)
        self.assertEqual(ampl.param["n_min"]["B1"], 100)
        self.assertEqual(ampl.param["n_min"]["B2"], 60)
        self.assertEqual(ampl.param["n_max"]["A"], 20000)
        self.assertEqual(ampl.param["n_max"]["C"], 3000)
        self.assertEqual(ampl.param["n_max"]["B1"], 777)
        self.assertEqual(ampl.param["n_max"]["B2"], 500)

    def test_to_pandas(self):
        try:
            import pandas as pd
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pandas and pyarrow are required")

        # nindices=1: first column becomes a named pandas index
        df = pd.DataFrame(
            {"val": [10.0, 20.0, 30.0]},
            index=pd.Index(["a", "b", "c"], name="key"),
        )
        dfa = DataFrameArrow.from_pandas(df)
        result = dfa.to_pandas()
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(result.index.name, "key")
        self.assertEqual(list(result.index), ["a", "b", "c"])
        self.assertEqual(list(result["val"]), [10.0, 20.0, 30.0])

        # nindices=2: index is a proper MultiIndex (nlevels=2)
        pairs = [("x", 1), ("x", 2), ("y", 1)]
        df_multi = pd.DataFrame(
            {"score": [1.0, 2.0, 3.0]},
            index=pd.MultiIndex.from_tuples(pairs, names=["letter", "num"]),
        )
        dfa_multi = DataFrameArrow.from_pandas(df_multi)
        result_multi = dfa_multi.to_pandas()
        self.assertEqual(result_multi.index.nlevels, 2)
        self.assertIsInstance(result_multi.index[0], tuple)
        self.assertEqual(len(result_multi), 3)
        self.assertIn("score", result_multi.columns)

        # nindices=0: no index promotion, all columns stay flat
        df_flat = pd.DataFrame(
            {"a": [1.0, 2.0], "b": [3.0, 4.0]},
            index=pd.Index(["p", "q"], name="idx"),
        )
        dfa_flat = DataFrameArrow.from_pandas(df_flat, indexarity=0)
        result_flat = dfa_flat.to_pandas()
        self.assertEqual(len(result_flat.columns), 3)  # idx + a + b

    def test_to_polars(self):
        try:
            import polars as pl
        except ImportError:
            self.skipTest("polars not available")
        try:
            import pandas as pd
        except ImportError:
            self.skipTest("pandas not available")

        # basic: single named index, one value column
        df = pd.DataFrame(
            {"val": [10.0, 20.0, 30.0]},
            index=pd.Index(["a", "b", "c"], name="key"),
        )
        dfa = DataFrameArrow.from_pandas(df)
        result = dfa.to_polars()
        self.assertIsInstance(result, pl.DataFrame)
        # polars has no index; key and val are both columns
        self.assertIn("key", result.columns)
        self.assertIn("val", result.columns)
        self.assertEqual(len(result), 3)
        self.assertEqual(sorted(result["key"].to_list()), ["a", "b", "c"])

        # multiple numeric columns
        df2 = pd.DataFrame(
            {"p1": [1.0, 2.0, 3.0], "p2": [4.0, 5.0, 6.0]},
            index=pd.Index([10, 20, 30], name="idx"),
        )
        dfa2 = DataFrameArrow.from_pandas(df2)
        result2 = dfa2.to_polars()
        self.assertIsInstance(result2, pl.DataFrame)
        self.assertEqual(len(result2), 3)
        self.assertIn("p1", result2.columns)
        self.assertIn("p2", result2.columns)
        self.assertEqual(sorted(result2["p1"].to_list()), [1.0, 2.0, 3.0])

        # string index + symbolic column
        df3 = pd.DataFrame(
            {"label": ["alpha", "beta", "gamma"], "score": [1.0, 2.0, 3.0]},
            index=pd.Index(["k0", "k1", "k2"], name="key"),
        )
        dfa3 = DataFrameArrow.from_pandas(df3)
        result3 = dfa3.to_polars()
        self.assertIsInstance(result3, pl.DataFrame)
        self.assertEqual(len(result3), 3)
        self.assertIn("label", result3.columns)
        self.assertIn("score", result3.columns)

        # multi-index: index levels become regular polars columns
        pairs = list(itertools.product(["A", "B", "C"], [1, 2, 3]))
        df_multi = pd.DataFrame(
            {
                "cost": [float(ord(p) - ord("A") + 1) * r for p, r in pairs],
                "qty":  [float(10 * (ord(p) - ord("A") + 1) + r) for p, r in pairs],
            },
            index=pd.MultiIndex.from_tuples(pairs, names=["product", "region"]),
        )
        dfa_multi = DataFrameArrow.from_pandas(df_multi)
        result_multi = dfa_multi.to_polars()
        self.assertIsInstance(result_multi, pl.DataFrame)
        self.assertEqual(len(result_multi), 9)
        self.assertIn("product", result_multi.columns)
        self.assertIn("region", result_multi.columns)
        self.assertIn("cost", result_multi.columns)
        self.assertIn("qty", result_multi.columns)
        # spot-check a value: product="B" (ord 2), region=3 → cost=6.0
        row = result_multi.filter(
            (pl.col("product") == "B") & (pl.col("region") == 3)
        )
        self.assertEqual(len(row), 1)
        self.assertAlmostEqual(row["cost"][0], 6.0, places=5)
        self.assertAlmostEqual(row["qty"][0], 23.0, places=5)

    def test_to_dict(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pyarrow not available")

        # single index, single value column
        dfa = DataFrameArrow.from_dict({"a": 1.0, "b": 2.0, "c": 3.0})
        result = dfa.to_dict()
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})

        # single index, multiple value columns
        dfa2 = DataFrameArrow.from_dict(
            {"x": (10.0, 100.0), "y": (20.0, 200.0)},
            column_names=["p", "q"],
        )
        result2 = dfa2.to_dict()
        self.assertEqual(result2["x"], (10.0, 100.0))
        self.assertEqual(result2["y"], (20.0, 200.0))

        # multi-index
        dfa3 = DataFrameArrow.from_dict(
            {("A", 1): 5.0, ("A", 2): 6.0, ("B", 1): 7.0},
            index_names=["prod", "region"],
            column_names=["cost"],
        )
        result3 = dfa3.to_dict()
        self.assertAlmostEqual(result3[("A", 1)], 5.0)
        self.assertAlmostEqual(result3[("B", 1)], 7.0)

    def test_to_list(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pyarrow not available")

        # single column total → scalar per row
        dfa = DataFrameArrow.from_dict({"a": 1.0, "b": 2.0, "c": 3.0})
        result = dfa.to_list()
        self.assertEqual(sorted(result), [("a", 1.0), ("b", 2.0), ("c", 3.0)])

        # skip_index with one value column → list of scalars
        dfa2 = DataFrameArrow.from_dict({"a": 1.0, "b": 2.0, "c": 3.0})
        vals = dfa2.to_list(skip_index=True)
        self.assertEqual(sorted(vals), [1.0, 2.0, 3.0])

        # multiple value columns → list of tuples; skip_index slices off index
        dfa3 = DataFrameArrow.from_dict(
            {"x": (10.0, 100.0), "y": (20.0, 200.0)},
            column_names=["p", "q"],
        )
        full = dfa3.to_list()
        self.assertEqual(len(full), 2)
        self.assertIn(("x", 10.0, 100.0), full)

        dfa4 = DataFrameArrow.from_dict(
            {"x": (10.0, 100.0), "y": (20.0, 200.0)},
            column_names=["p", "q"],
        )
        vals_only = dfa4.to_list(skip_index=True)
        self.assertIn((10.0, 100.0), vals_only)

    def test_from_dict(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pyarrow not available")

        # scalar keys and values, default names
        dfa = DataFrameArrow.from_dict({"a": 1.0, "b": 2.0, "c": 3.0})
        self.assertIsInstance(dfa, DataFrameArrow)

        # custom names roundtrip
        data = {"x": (10.0, "alpha"), "y": (20.0, "beta")}
        dfa2 = DataFrameArrow.from_dict(
            data,
            index_names=["key"],
            column_names=["val", "label"],
        )
        result = dfa2.to_dict()
        self.assertEqual(result["x"], (10.0, "alpha"))
        self.assertEqual(result["y"], (20.0, "beta"))

        # multi-index keys
        dfa3 = DataFrameArrow.from_dict(
            {("A", 1): 5.0, ("B", 2): 6.0},
            index_names=["prod", "region"],
            column_names=["cost"],
        )
        result3 = dfa3.to_dict()
        self.assertAlmostEqual(result3[("A", 1)], 5.0)
        self.assertAlmostEqual(result3[("B", 2)], 6.0)

    def test_from_list(self):
        try:
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pyarrow not available")

        # basic roundtrip: single index, single value column
        rows = [("a", 1.0), ("b", 2.0), ("c", 3.0)]
        dfa = DataFrameArrow.from_list(rows, index_names=["key"], column_names=["val"])
        result = dfa.to_dict()
        self.assertEqual(result, {"a": 1.0, "b": 2.0, "c": 3.0})

        # multi-index, two value columns
        rows2 = [("A", 1, 5.0, 50.0), ("A", 2, 6.0, 60.0), ("B", 1, 7.0, 70.0)]
        dfa2 = DataFrameArrow.from_list(
            rows2,
            index_names=["prod", "region"],
            column_names=["cost", "qty"],
        )
        result2 = dfa2.to_dict()
        self.assertEqual(result2[("A", 1)], (5.0, 50.0))
        self.assertEqual(result2[("B", 1)], (7.0, 70.0))

        # to_list roundtrip
        rows3 = [("x", 10.0), ("y", 20.0)]
        dfa3 = DataFrameArrow.from_list(rows3, index_names=["k"], column_names=["v"])
        self.assertEqual(sorted(dfa3.to_list()), [("x", 10.0), ("y", 20.0)])

    def test_getdata_arrow(self):
        try:
            import pyarrow as pa
        except ImportError:
            self.skipTest("pyarrow not available")

        ampl = self.ampl
        ampl.eval("set X := 1..3;")
        result = ampl.get_data("X")
        self.assertIsInstance(result, DataFrameArrow)
        df = result.to_pandas()
        self.assertEqual(len(df), 3)

        # multiple statements with indexed params
        ampl.reset()
        ampl.eval(
            """
        param p1{i in 1..10} := 1*i;
        param p2{i in 1..10} := 2*i;
        param p3{i in 0..10: i >= 1} := 3*i;
        """
        )
        result = ampl.get_data("p1", "p2", "p3")
        self.assertIsInstance(result, DataFrameArrow)
        df = result.to_pandas()
        self.assertEqual(len(df), 10)
        self.assertIn("p1", df.columns)
        self.assertIn("p2", df.columns)
        self.assertIn("p3", df.columns)
        self.assertEqual(list(df["p1"]), [float(i) for i in range(1, 11)])
        self.assertEqual(list(df["p2"]), [float(2 * i) for i in range(1, 11)])
        self.assertEqual(list(df["p3"]), [float(3 * i) for i in range(1, 11)])

        # symbolic (string) set members
        ampl.reset()
        ampl.eval(
            """
        set CITIES := {"Berlin", "Paris", "Rome"};
        param pop{c in CITIES} :=
          if c = "Berlin" then 3.6
          else if c = "Paris" then 2.1
          else 2.8;
        """
        )
        result = ampl.get_data("pop")
        self.assertIsInstance(result, DataFrameArrow)
        df = result.to_pandas()
        self.assertEqual(len(df), 3)
        self.assertIn("pop", df.columns)
        cities_col = list(df.index)
        self.assertIn("Berlin", cities_col)
        self.assertIn("Paris", cities_col)
        self.assertIn("Rome", cities_col)

    def test_arrow_pandas_roundtrip(self):
        try:
            import pandas as pd
            import pyarrow  # noqa: F401
        except ImportError:
            self.skipTest("pandas and pyarrow are required")

        ampl = self.ampl

        # ── numeric params, integer index ──────────────────────────────────────
        ampl.eval(
            """
        set S;
        param p1{S};
        param p2{S};
        param p3{S};
        """
        )
        df_in = pd.DataFrame(
            {
                "p1": [float(i) for i in range(1, 11)],
                "p2": [float(2 * i) for i in range(1, 11)],
                "p3": [float(3 * i) for i in range(1, 11)],
            },
            index=pd.Index(range(1, 11), name="key"),
        )
        ampl.set_data(df_in, "S")

        result = ampl.get_data("p1", "p2", "p3")
        self.assertIsInstance(result, DataFrameArrow)
        df_out = result.to_pandas()
        df_out = df_out.sort_index()

        self.assertEqual(len(df_out), 10)
        self.assertIn("p1", df_out.columns)
        self.assertIn("p2", df_out.columns)
        self.assertIn("p3", df_out.columns)
        self.assertEqual(list(df_out["p1"]), [float(i) for i in range(1, 11)])
        self.assertEqual(list(df_out["p2"]), [float(2 * i) for i in range(1, 11)])
        self.assertEqual(list(df_out["p3"]), [float(3 * i) for i in range(1, 11)])

        # ── string index ───────────────────────────────────────────────────────
        ampl.reset()
        ampl.eval(
            """
        set CITIES;
        param population{CITIES};
        param area{CITIES};
        """
        )
        cities = ["Berlin", "Paris", "Rome", "Madrid"]
        df_cities = pd.DataFrame(
            {
                "population": [3.6, 2.1, 2.8, 3.3],
                "area": [891.8, 105.4, 1285.0, 604.3],
            },
            index=pd.Index(cities, name="city"),
        )
        ampl.set_data(df_cities, "CITIES")

        result = ampl.get_data("population", "area")
        df_out = result.to_pandas().sort_index()

        self.assertEqual(len(df_out), 4)
        self.assertEqual(sorted(list(df_out.index)), sorted(cities))
        self.assertAlmostEqual(
            df_out.loc["Berlin", "population"], 3.6, places=5
        )
        self.assertAlmostEqual(df_out.loc["Paris", "area"], 105.4, places=5)

        # ── symbolic (string-valued) param ────────────────────────────────────
        ampl.reset()
        ampl.eval(
            """
        set S;
        param label{S} symbolic;
        param value{S};
        """
        )
        keys = [f"k{i}" for i in range(5)]
        df_sym = pd.DataFrame(
            {
                "label": ["alpha", "beta", "gamma", "delta", "epsilon"],
                "value": [1.0, 2.0, 3.0, 4.0, 5.0],
            },
            index=pd.Index(keys, name="key"),
        )
        ampl.set_data(df_sym, "S")

        result = ampl.get_data("label", "value")
        df_out = result.to_pandas().sort_index()

        self.assertEqual(len(df_out), 5)
        self.assertEqual(list(df_out.index), sorted(keys))
        self.assertIn("label", df_out.columns)
        self.assertEqual(list(df_out["value"]), [1.0, 2.0, 3.0, 4.0, 5.0])
        label_map = dict(zip(df_out.index, df_out["label"]))
        self.assertEqual(label_map["k0"], "alpha")
        self.assertEqual(label_map["k4"], "epsilon")

        # ── multi-index (2 index columns) ──────────────────────────────────────
        ampl.reset()
        ampl.eval(
            """
        set PRODUCTS := {"A", "B", "C"};
        set REGIONS  := {1, 2, 3};
        param cost{PRODUCTS, REGIONS};
        param qty{PRODUCTS, REGIONS};
        """
        )
        products = ["A", "B", "C"]
        regions = [1, 2, 3]
        pairs = list(itertools.product(products, regions))
        df_multi = pd.DataFrame(
            {
                "cost": [float(ord(p) - ord("A") + 1) * r for p, r in pairs],
                "qty":  [float(10 * (ord(p) - ord("A") + 1) + r) for p, r in pairs],
            },
            index=pd.MultiIndex.from_tuples(pairs, names=["product", "region"]),
        )
        ampl.set_data(df_multi)

        result = ampl.get_data("cost", "qty")
        df_out = result.to_pandas()

        # result must be a proper MultiIndex (nlevels=2)
        self.assertEqual(df_out.index.nlevels, 2)
        self.assertIsInstance(df_out.index[0], tuple)
        self.assertEqual(len(df_out), len(pairs))
        self.assertIn("cost", df_out.columns)
        self.assertIn("qty", df_out.columns)

        # verify every (product, region) cell round-trips correctly
        df_in_sorted = df_multi.sort_index()
        for p, r in pairs:
            self.assertAlmostEqual(
                df_out.loc[(p, r), "cost"],
                df_in_sorted.loc[(p, r), "cost"],
                places=5,
            )
            self.assertAlmostEqual(
                df_out.loc[(p, r), "qty"],
                df_in_sorted.loc[(p, r), "qty"],
                places=5,
            )
