#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
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
        ampl.set_data_arrow(df, "S")
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
        ampl.set_data_arrow(df, "S")
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
        ampl.set_data_arrow(df2, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["x", "y", "z"])
        self.assertEqual(ampl.param["a"]["x"], 10)
        self.assertEqual(ampl.param["a"]["y"], 20)
        self.assertEqual(ampl.param["a"]["z"], 30)
        
        
        ampl.eval("reset data;")
        df3 = pd.DataFrame({}, index=["xx", "yy"])
        ampl.set_data_arrow(df3, "S")
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
        ampl.set_data_arrow(nutr_df, "NUTR")
        self.assertEqual(list(ampl.set["NUTR"].members()), ["A", "C", "B1", "B2"])
        self.assertEqual(ampl.param["n_min"]["A"], 700)
        self.assertEqual(ampl.param["n_min"]["C"], 500)
        self.assertEqual(ampl.param["n_min"]["B1"], 100)
        self.assertEqual(ampl.param["n_min"]["B2"], 60)
        self.assertEqual(ampl.param["n_max"]["A"], 20000)
        self.assertEqual(ampl.param["n_max"]["C"], 3000)
        self.assertEqual(ampl.param["n_max"]["B1"], 777)
        self.assertEqual(ampl.param["n_max"]["B2"], 500)

