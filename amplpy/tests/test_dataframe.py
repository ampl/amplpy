#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import string
import random
import os
from amplpy import DataFrame
from . import TestBase

try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None


class TestDataFrame(TestBase.TestBase):
    """Test DataFrame."""

    def test_dataframe(self):
        # Create first dataframe (for data indexed over NUTR)
        # Add data row by row
        df1 = DataFrame("NUTR", ("n_min", "n_max"))
        df1._add_row(("A", 700, 20000))
        df1._add_row(("B1", 700, 20000))
        df1._add_row(("B2", 700, 20000))
        df1._add_row(("C", 700, 20000))
        df1._add_row(("CAL", 16000, 24000))
        df1._add_row(("NA", 0.0, 50000))

        # Create second dataframe (for data indexed over FOOD)
        # Add column by column
        df2 = DataFrame("FOOD")
        foods = ["BEEF", "CHK", "FISH", "HAM", "MCH", "MTL", "SPG", "TUR"]
        df2._set_column("FOOD", foods)
        self.assertEqual(list(df2._get_column("FOOD")), foods)
        contents = [2] * 8
        df2._add_column("f_min", contents)
        self.assertEqual(list(df2._get_column("f_min")), contents)
        contents = [10] * 8
        df2._add_column("f_max", contents)
        self.assertEqual(list(df2._get_column("f_max")), contents)
        costs = [3.19, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49]
        df2._add_column("cost", costs)
        self.assertEqual(list(df2._get_column("cost")), costs)
        labels = [random.choice(string.ascii_letters)] * 8
        df2._add_column("labels", labels)
        self.assertEqual(list(df2._get_column("labels")), labels)
        df2._add_column("empty", [])
        self.assertEqual(list(df2._get_column("empty")), [None] * 8)

        print(df2._get_column("FOOD"))
        for index in df2._get_column("FOOD"):
            print(df2._get_row(index))

        # Create third dataframe, to assign data to the AMPL entity
        # param amt{NUTR, FOOD};
        df3 = DataFrame(("NUTR", "FOOD"))
        # Populate the set columns
        nutr_with_multiplicity = [""] * 48
        food_with_multiplicity = [""] * 48
        i = 0
        for n in range(6):
            for f in range(8):
                print(df1._get_row_by_index(n)[0])
                nutr_with_multiplicity[i] = df1._get_row_by_index(n)[0]
                food_with_multiplicity[i] = foods[f]
                i += 1
        df3._set_column("NUTR", nutr_with_multiplicity)
        df3._set_column("FOOD", food_with_multiplicity)

        # Populate with all these values
        values = [
            60,
            8,
            8,
            40,
            15,
            70,
            25,
            60,
            10,
            20,
            15,
            35,
            15,
            15,
            25,
            15,
            15,
            20,
            10,
            10,
            15,
            15,
            15,
            10,
            20,
            0,
            10,
            40,
            35,
            30,
            50,
            20,
            295,
            770,
            440,
            430,
            315,
            400,
            370,
            450,
            968,
            2180,
            945,
            278,
            1182,
            896,
            1329,
            1397,
        ]
        df3._add_column("amt", values)

    def test_pandas(self):
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
        ampl.set_data(df, "S")
        self.assertEqual(list(ampl.set["S"].members()), ["x", "y"])
        self.assertEqual(ampl.param["a"]["x"], 1)
        self.assertEqual(ampl.param["b"]["y"], 4)

        df2 = pd.DataFrame(
            {
                "a": [10, 20, 30],
            },
            index=["x", "y", "z"],
        )
        df3 = pd.DataFrame({}, index=["xx", "yy"])
        df = DataFrame.from_pandas(df)
        df2 = DataFrame.from_pandas(df2)
        df3 = DataFrame.from_pandas(df3)
        self.assertTrue(isinstance(df.to_dict(), dict))
        self.assertTrue(isinstance(df.to_list(), list))
        self.assertTrue(isinstance(df.to_pandas(), pd.DataFrame))

        self.assertEqual(df.to_list()[0][1:], (1, 3.5))
        self.assertEqual(df2.to_list()[0], ("x", 10))
        self.assertEqual(df3.to_list()[0], "xx")

        self.assertEqual(set(df.to_dict().keys()), set(["x", "y"]))
        self.assertEqual(set(df2.to_dict().keys()), set(["x", "y", "z"]))
        self.assertEqual(set(df3.to_dict().keys()), set(["xx", "yy"]))

        self.assertEqual(df.to_dict()["x"], (1, 3.5))
        self.assertEqual(df2.to_dict()["x"], 10)
        self.assertEqual(df3.to_dict()["xx"], None)

        csv_file = os.path.join(os.path.dirname(__file__), "data.csv")
        p_df = pd.read_csv(csv_file, sep=";", index_col=0)
        df = DataFrame.from_pandas(p_df)
        self.assertTrue(isinstance(df.to_dict(), dict))
        self.assertEqual(set(df.to_dict().keys()), set([1.0, 2.0, 3.0]))
        self.assertEqual(set(df.to_list()[0]), set([1.0, 0.01]))
        self.assertEqual(set(df.to_list()[1]), set([2.0, 0.02]))
        self.assertEqual(set(df.to_list()[2]), set([3.0, 0.03]))

    def test_pandas_advanced(self):
        ampl = self.ampl
        if pd is None:
            self.skipTest("pandas not available")
        ampl.eval(
            """
            set someSet := {"First", "Second"};
            param N := 5;
            param x1{someSet, 1..N} default 0;
            param x2{someSet, 1..N} default 0;
            param x3{someSet, 1..N} default 0;
            param x4{someSet, 1..N} default 0;
        """
        )

        df = pd.DataFrame(
            [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0]],
            index=["First", "Second"],
            columns=[1, 2, 3, 4, 5],
        )
        ampl.param["x1"] = pd.DataFrame.from_dict(
            df.stack().to_dict(), orient="index", columns=["v"]
        )
        ampl.param["x2"] = pd.DataFrame(df.stack())
        ampl.param["x3"] = df.stack().to_dict()
        ampl.param["x4"] = df.stack()
        d1 = ampl.param["x1"].get_values().to_dict()
        d2 = ampl.param["x2"].get_values().to_dict()
        d3 = ampl.param["x3"].get_values().to_dict()
        d4 = ampl.param["x4"].get_values().to_dict()
        self.assertEqual(d1, d2)
        self.assertEqual(d2, d3)
        self.assertEqual(d3, d4)

    def test_pandas_named_columns(self):
        if pd is None:
            self.skipTest("pandas not available")
        df_unindexed = pd.DataFrame(
            [
                ["Apple", "Red", 3, 1.29],
                ["Apple", "Green", 9, 0.99],
                ["Pear", "Red", 25, 2.59],
                ["Pear", "Green", 26, 2.79],
                ["Lime", "Green", 99, 0.39],
            ],
            columns=["Fruit", "Color", "Count", "Price"],
        )
        # RangeIndex
        self.assertEqual(
            DataFrame.from_pandas(df_unindexed)._get_headers(),
            ("index0", "Fruit", "Color", "Count", "Price"),
        )

        # MultiIndex
        df_indexed = df_unindexed.set_index(["Fruit", "Color"])
        self.assertEqual(
            DataFrame.from_pandas(
                df_indexed, index_names=["Fruit", "Color"]
            )._get_headers(),
            ("Fruit", "Color", "Count", "Price"),
        )

        # Index without name
        df = pd.DataFrame(
            [[1, 2, 3, 4, 5], [6, 7, 8, 9, 0]],
            index=["First", "Second"],
            columns=[1, 2, 3, 4, 5],
        )
        self.assertEqual(
            DataFrame.from_pandas(df.stack())._get_headers(), ("index0", "index1", "0")
        )

    def test_pandas_multi_index(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval("param p{i in 1..100, j in 1..100} := i*j;")
        df1 = ampl.get_data("p").to_pandas()
        self.assertEqual(df1.index.nlevels, 2)
        df2 = ampl.get_data("p").to_pandas(multi_index=False)
        self.assertEqual(df2.index.nlevels, 1)
        self.assertEqual(df1.index.to_list(), df2.index.to_list())

    def test_numpy(self):
        ampl = self.ampl
        if np is None:
            self.skipTest("numpy not available")
        ampl.eval("set X;")
        arr = np.array([1, 2, 3])
        ampl.set["X"] = arr
        self.assertEqual(list(ampl.set["X"].members()), [1, 2, 3])
        ampl.eval("param p{1..3};")
        ampl.param["p"] = arr
        self.assertEqual(ampl.param["p"][2], 2)
        self.assertEqual(DataFrame.from_numpy(arr).to_list(), [1, 2, 3])
        mat = np.array([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(DataFrame.from_numpy(mat).to_list(), [(1, 2), (3, 4), (5, 6)])
        self.assertEqual(DataFrame.from_numpy(mat[:, 0]).to_list(), [1, 3, 5])
        self.assertEqual(DataFrame.from_numpy(mat[:, 1]).to_list(), [2, 4, 6])

    def test_dict(self):
        dic = {"aa": "bb", "c": "a"}
        self.assertEqual(dic, DataFrame.from_dict(dic).to_dict())
        dic = {1: 2}
        self.assertEqual(dic, DataFrame.from_dict(dic).to_dict())
        dic = {1: 2, 3: 4}
        self.assertEqual(dic, DataFrame.from_dict(dic).to_dict())
        dic = {2.0: ("a", "b"), 3: ("1", "2")}
        self.assertEqual(dic, DataFrame.from_dict(dic).to_dict())
        dic = {(2.0, "c"): ("a", "b"), (3, "a"): ("1", "2")}
        self.assertEqual(dic, DataFrame.from_dict(dic).to_dict())
        df = DataFrame("x", "y")
        dic = {1: 12, 2: 23}
        df._set_values(dic)
        self.assertEqual(dic, df.to_dict())
        df = DataFrame("x", ["y", "z"])
        dic = {1: (12, 2), 2: (23, -1)}
        df._set_values(dic)
        self.assertEqual(dic, df.to_dict())
        df = DataFrame("x", ["y", "z"])
        df._set_values({1: [1, 2]})
        self.assertEqual({1: (1, 2)}, df.to_dict())

    def test_no_index(self):
        if pd is None:
            self.skipTest("pandas not available")
        df = DataFrame([], ["x", "y"])
        x = [1, 2, 3]
        y = [4, 5, 6]
        df._set_column("x", x)
        df._set_column("y", y)
        with self.assertRaises(ValueError):
            df.to_dict()
        pd_df = df.to_pandas()
        self.assertEqual(list(pd_df["x"]), x)
        self.assertEqual(list(pd_df["y"]), y)

    def test_iter(self):
        df = DataFrame("x", "y")
        dic = {1: 12, 2: 23}
        df._set_values(dic)
        for row in df:
            self.assertTrue(tuple(row) in [(1, 12), (2, 23)])

    def test_integer_values(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        df1 = ampl.get_data("{i in 1..2, j in 1..2} i*j/2")
        df1_pd = df1.to_pandas()
        df2 = ampl.get_data("{i in 1..2, j in 1..2} i*j")
        df2_pd = df2.to_pandas()

        self.assertEqual(df1_pd.index.tolist(), [(1, 1), (1, 2), (2, 1), (2, 2)])
        self.assertEqual(df1_pd["i*j/2"].tolist(), [0.5, 1.0, 1.0, 2.0])

        self.assertEqual(df2_pd.index.tolist(), [(1, 1), (1, 2), (2, 1), (2, 2)])
        self.assertEqual(df2_pd["i*j"].tolist(), [1, 2, 2, 4])

        self.assertEqual(df1.to_dict(), {(1, 1): 0.5, (1, 2): 1, (2, 1): 1, (2, 2): 2})
        self.assertEqual(df2.to_dict(), {(1, 1): 1, (1, 2): 2, (2, 1): 2, (2, 2): 4})

        self.assertEqual(df1.to_list(), [(1, 1, 0.5), (1, 2, 1), (2, 1, 1), (2, 2, 2)])
        self.assertEqual(df2.to_list(), [(1, 1, 1), (1, 2, 2), (2, 1, 2), (2, 2, 4)])


if __name__ == "__main__":
    unittest.main()
