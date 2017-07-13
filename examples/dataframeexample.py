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
        # Create first dataframe (for data indexed over NUTR)
        # Add data row by row
        df1 = DataFrame('NUTR', ('n_min', 'n_max'))
        df1.addRow('A', 700, 20000)
        df1.addRow('B1', 700, 20000)
        df1.addRow('B2', 700, 20000)
        df1.addRow('C', 700, 20000)
        df1.addRow('CAL', 16000, 24000)
        df1.addRow('NA', 0.0, 50000)

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

        # Create third dataframe, to assign data to the AMPL entity
        # param amt{NUTR, FOOD};
        df3 = DataFrame(index=('NUTR', 'FOOD'))
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

        # Create AMPL object
        ampl = AMPL()

        if argc > 1:
            ampl.setOption('solver', argv[1])

        # Read the model file
        modelDirectory = argv[2] if argc == 3 else os.path.join('..', 'models')
        ampl.read(os.path.join(modelDirectory, 'diet/diet.mod'))

        # Assign data to NUTR, n_min and n_max
        ampl.setData(df1, 'NUTR')
        # Assign data to FOOD, f_min, f_max and cost
        ampl.setData(df2, 'FOOD')
        # Assign data to amt
        ampl.setData(df3)
        # Solve the model
        ampl.solve()

        # Print out the result
        print(
            "Objective function value: {}".format(
                ampl.getObjective('total_cost').value()
            )
        )

        # Get the values of the variable Buy in a dataframe
        results = ampl.getVariable('Buy').getValues()
        # Print
        print(results)
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
