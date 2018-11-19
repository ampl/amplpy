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
        ampl = self.ampl
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
        ampl.eval('''
            set S;
            param a{S};
            param b{S};
        ''')
        ampl.setData(df, 'S')
        self.assertEqual(list(ampl.set['S'].members()), ['x', 'y'])
        self.assertEqual(ampl.param['a']['x'], 1)
        self.assertEqual(ampl.param['a']['y'], 2)
        df2 = pd.DataFrame({
            'a': [10, 20, 30],
        },
            index=['x', 'y', 'z']
        )
        df3 = pd.DataFrame({}, index=['xx', 'yy'])
        df = DataFrame.fromPandas(df)
        df2 = DataFrame.fromPandas(df2)
        df3 = DataFrame.fromPandas(df3)
        self.assertTrue(isinstance(df.toDict(), dict))
        self.assertTrue(isinstance(df.toList(), list))
        self.assertTrue(isinstance(df.toPandas(), pd.DataFrame))

        self.assertEqual(df.toList()[0][1:], (1, 3.5))
        self.assertEqual(df2.toList()[0], ('x', 10))
        self.assertEqual(df3.toList()[0], 'xx')

        self.assertEqual(set(df.toDict().keys()), set(['x', 'y']))
        self.assertEqual(set(df2.toDict().keys()), set(['x', 'y', 'z']))
        self.assertEqual(set(df3.toDict().keys()), set(['xx', 'yy']))

        self.assertEqual(df.toDict()['x'], (1, 3.5))
        self.assertEqual(df2.toDict()['x'], 10)
        self.assertEqual(df3.toDict()['xx'], None)

        csv_file = os.path.join(os.path.dirname(__file__), 'data.csv')
        p_df = pd.read_table(csv_file, sep=';', index_col=0)
        df = DataFrame.fromPandas(p_df)
        self.assertTrue(isinstance(df.toDict(), dict))
        self.assertEqual(set(df.toDict().keys()), set([1.0, 2.0, 3.0]))
        self.assertEqual(set(df.toList()[0]), set([1.0, 0.01]))
        self.assertEqual(set(df.toList()[1]), set([2.0, 0.02]))
        self.assertEqual(set(df.toList()[2]), set([3.0, 0.03]))

    def testPandasAdvanced(self):
        ampl = self.ampl
        try:
            import pandas as pd
        except ImportError:
            return
        ampl.eval('''
            set someSet := {"First", "Second"};
            param N := 5;
            param x1{someSet, 1..N} default 0;
            param x2{someSet, 1..N} default 0;
            param x3{someSet, 1..N} default 0;
            param x4{someSet, 1..N} default 0;
        ''')

        df = pd.DataFrame([
                [1, 2, 3, 4, 5],
                [6, 7, 8, 9, 0]
            ],
            index=['First', 'Second'],
            columns=[1, 2, 3, 4, 5]
        )
        ampl.param['x1'] = pd.DataFrame.from_dict(
            df.stack().to_dict(),
            orient='index',
            columns=['v']
        )
        ampl.param['x2'] = pd.DataFrame(df.stack())
        ampl.param['x3'] = df.stack().to_dict()
        ampl.param['x4'] = df.stack()
        d1 = ampl.param['x1'].getValues().toDict()
        d2 = ampl.param['x2'].getValues().toDict()
        d3 = ampl.param['x3'].getValues().toDict()
        d4 = ampl.param['x4'].getValues().toDict()
        self.assertEqual(d1, d2)
        self.assertEqual(d2, d3)
        self.assertEqual(d3, d4)

    def testNumpy(self):
        ampl = self.ampl
        try:
            import numpy as np
        except ImportError:
            return
        ampl.eval('set X;')
        arr = np.array([1, 2, 3])
        ampl.set['X'] = arr
        self.assertEqual(list(ampl.set['X'].members()), [1, 2, 3])
        ampl.eval('param p{1..3};')
        ampl.param['p'] = arr
        self.assertEqual(ampl.param['p'][2], 2)
        self.assertEqual(
            DataFrame.fromNumpy(arr).toList(),
            [1, 2, 3]
        )
        mat = np.matrix([[1, 2], [3, 4], [5, 6]])
        self.assertEqual(
            DataFrame.fromNumpy(mat).toList(),
            [(1, 2), (3, 4), (5, 6)]
        )
        self.assertEqual(
            DataFrame.fromNumpy(mat[:, 0]).toList(),
            [1, 3, 5]
        )
        self.assertEqual(
            DataFrame.fromNumpy(mat[:, 1]).toList(),
            [2, 4, 6]
        )


if __name__ == '__main__':
    unittest.main()
