#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL
    os.chdir(os.path.dirname(__file__) or os.curdir)
    try:
        ampl = AMPL()

        if argc > 1:
            ampl.setOption('solver', argv[1])

        # Read the model and data files.
        modelDirectory = argv[2] if argc == 3 else os.path.join('..', 'models')
        ampl.read(os.path.join(modelDirectory, 'diet/diet.mod'))
        ampl.readData(os.path.join(modelDirectory, 'diet/diet.dat'))

        # Solve
        ampl.solve()

        # Get objective entity by AMPL name
        totalcost = ampl.getObjective('total_cost')
        # Print it
        print("Objective is:", totalcost.value())

        # Reassign data - specific instances
        cost = ampl.getParameter('cost')
        cost.setValues({'BEEF': 5.01, 'HAM': 4.55})
        print("Increased costs of beef and ham.")

        # Resolve and display objective
        ampl.solve()
        print("New objective value:", totalcost.value())

        # Reassign data - all instances
        elements = [3, 5, 5, 6, 1, 2, 5.01, 4.55]
        cost.setValues(elements)
        print("Updated all costs.")

        # Resolve and display objective
        ampl.solve()
        print("New objective value:", totalcost.value())

        # Get the values of the variable Buy in a dataframe object
        buy = ampl.getVariable('Buy')
        df = buy.getValues()
        # Print them
        print(df)

        # Get the values of an expression into a DataFrame object
        df2 = ampl.getData('{j in FOOD} 100*Buy[j]/Buy[j].ub')
        # Print them
        print(df2)
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
