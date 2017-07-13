#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL, DataFrame
    os.chdir(os.path.dirname(__file__) or os.curdir)
    try:
        ampl = AMPL()

        if argc > 1:
            ampl.setOption('solver', argv[1])

        # Read the model file
        modelDirectory = argv[2] if argc == 3 else os.path.join('..', 'models')
        ampl.read(os.path.join(modelDirectory, 'diet/diet.mod'))

        foods = ['BEEF', 'CHK', 'FISH', 'HAM', 'MCH', 'MTL', 'SPG', 'TUR']
        costs = [3.59, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49]

        fmin = [2, 2, 2, 2, 2, 2, 2, 2]
        fmax = [10, 10, 10, 10, 10, 10, 10, 10]

        df = DataFrame('FOOD')
        df.setColumn('FOOD', foods)
        df.addColumn('cost', costs)
        df.addColumn('f_min', fmin)
        df.addColumn('f_max', fmax)
        ampl.setData(df, 'FOOD')

        nutrients = ['A', 'C', 'B1', 'B2', 'NA', 'CAL']
        nmin = [700, 700, 700, 700, 0, 16000]
        nmax = [20000, 20000, 20000, 20000, 50000, 24000]

        df = DataFrame('NUTR')
        df.setColumn('NUTR', nutrients)
        df.addColumn('n_min', nmin)
        df.addColumn('n_max', nmax)
        ampl.setData(df, 'NUTR')

        amounts = [
            [ 60,    8,   8,  40,   15,  70,   25,   60],
            [ 20,    0,  10,  40,   35,  30,   50,   20],
            [ 10,   20,  15,  35,   15,  15,   25,   15],
            [ 15,   20,  10,  10,   15,  15,   15,   10],
            [928, 2180, 945, 278, 1182, 896, 1329, 1397],
            [295,  770, 440, 430,  315, 400,  379,  450]
        ]

        df = DataFrame(('NUTR', 'FOOD'), 'amt')
        df.setValues({
            (nutrient, food): amounts[i][j]
            for i, nutrient in enumerate(nutrients)
            for j, food in enumerate(foods)
        })
        ampl.setData(df)

        ampl.solve()

        print('Objective: {}'.format(ampl.getObjective('total_cost').value()))
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
