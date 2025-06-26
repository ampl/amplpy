#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import string
import random
import os
from amplpy import DataFrameArrow
from . import TestBase

#try:
#    import numpy as np
#except ImportError:
#    np = None
try:
    import pandas as pd
except ImportError:
    pd = None


class TestDataFrameArrow(TestBase.TestBase):
    """Test DataFrame."""

    def test_pandas_arrow(self):
        ampl = self.ampl
        if pd is None:
            self.skipTest("pandas not available")
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
        self.assertEqual(ampl.param["b"]["y"], 4)