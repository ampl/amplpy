#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

from . import TestBase
import unittest
from amplpy import DataFrame
import amplpy
import os


class TestDataFrame(TestBase.TestBase):
    """Test DataFrame."""

    def testDataFrame(self):
        ampl = self.ampl
        # Create first dataframe (for data indexed over NUTR)
        # Add data row by row
        df1 = DataFrame('NUTR', ('n_min', 'n_max'))
        df1.addRow(('A', 700, 20000))
        df1.addRow(('B1', 700, 20000))
        df1.addRow(('B2', 700, 20000))
        df1.addRow(('C', 700, 20000))
        df1.addRow(('CAL', 16000, 24000))
        df1.addRow(('NA', 0.0, 50000))

        # Create second dataframe (for data indexed over FOOD)
        # Add column by column
        df2 = DataFrame('FOOD')
        foods = ['BEEF', 'CHK', 'FISH', 'HAM', 'MCH', 'MTL', 'SPG', 'TUR']
        df2.setColumn('FOOD', foods)
        contents = [2] * 8
        df2.addColumn('f_min', contents)
        contents = [10] * 8
        df2.addColumn('f_max', contents)
        costs = [3.19, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49]
        df2.addColumn('cost', costs)

        print(df2.getColumn('FOOD'))
        for index in df2.getColumn('FOOD'):
            print(df2.getRow(index))

        # Create third dataframe, to assign data to the AMPL entity
        # param amt{NUTR, FOOD};
        df3 = DataFrame(('NUTR', 'FOOD'))
        # Populate the set columns
        nutrWithMultiplicity = ['']*48
        foodWithMultiplicity = ['']*48
        i = 0
        for n in range(6):
            for f in range(8):
                print(df1.getRowByIndex(n)[0])
                nutrWithMultiplicity[i] = df1.getRowByIndex(n)[0]
                foodWithMultiplicity[i] = foods[f]
                i += 1
        df3.setColumn('NUTR', nutrWithMultiplicity)
        df3.setColumn('FOOD', foodWithMultiplicity)

        # Populate with all these values
        values = [
            60, 8, 8, 40, 15, 70, 25, 60, 10, 20, 15, 35, 15, 15, 25, 15, 15,
            20, 10, 10, 15, 15, 15, 10, 20, 0, 10, 40, 35, 30, 50, 20, 295,
            770, 440, 430, 315, 400, 370, 450, 968, 2180, 945, 278, 1182, 896,
            1329, 1397
        ]
        df3.addColumn('amt', values)

    def testPandas(self):
        try:
            import pandas as pd
        except ImportError:
            return
        df = pd.DataFrame({
            'a': [1, 2],
            'b': [3.5, 4]
        },
            index=['x', 'y']
        )
        df = DataFrame.fromPandas(df)
        self.assertTrue(isinstance(df.toDict(), dict))
        self.assertTrue(isinstance(df.toList(), list))
        self.assertTrue(isinstance(df.toPandas(), pd.DataFrame))
        self.assertEqual(set(df.toDict().keys()), set(['x', 'y']))
        self.assertEqual(set(df.toList()[0][1:]), set([1, 3.5]))
        csv_file = os.path.join(os.path.dirname(__file__), 'data.csv')
        p_df = pd.read_table(csv_file, sep=';', index_col=0)
        df = DataFrame.fromPandas(p_df)
        self.assertTrue(isinstance(df.toDict(), dict))
        self.assertEqual(set(df.toDict().keys()), set([1.0, 2.0, 3.0]))
        self.assertEqual(set(df.toList()[0]), set([1.0, 0.01]))
        self.assertEqual(set(df.toList()[1]), set([2.0, 0.02]))
        self.assertEqual(set(df.toList()[2]), set([3.0, 0.03]))


if __name__ == '__main__':
    unittest.main()
