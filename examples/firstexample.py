#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL
    os.chdir(os.path.dirname(__file__) or os.curdir)

    # Create an AMPL instance
    ampl = AMPL()

    '''
    # If the AMPL installation directory is not in the system search path:
    from amplpy import Environment
    ampl = AMPL(
        Environment('full path to the AMPL installation directory'))
    '''

    if argc > 1:
        ampl.set_option('solver', argv[1])

    # Read the model and data files.
    model_directory = argv[2] if argc == 3 else os.path.join('..', 'models')
    ampl.read(os.path.join(model_directory, 'diet/diet.mod'))
    ampl.read_data(os.path.join(model_directory, 'diet/diet.dat'))

    # Solve
    ampl.solve()

    # Get objective entity by AMPL name
    totalcost = ampl.get_objective('Total_Cost')
    # Print it
    print('Objective is:', totalcost.value())

    # Reassign data - specific instances
    cost = ampl.get_parameter('cost')
    cost.set_values({'BEEF': 5.01, 'HAM': 4.55})
    print('Increased costs of beef and ham.')

    # Resolve and display objective
    ampl.solve()
    print('New objective value:', totalcost.value())

    # Reassign data - all instances
    elements = [3, 5, 5, 6, 1, 2, 5.01, 4.55]
    cost.set_values(elements)
    print('Updated all costs.')

    # Resolve and display objective
    ampl.solve()
    print('New objective value:', totalcost.value())

    # Get the values of the variable Buy in a dataframe object
    buy = ampl.get_variable('Buy')
    df = buy.get_values()
    # Print them
    print(df)

    # Get the values of an expression into a DataFrame object
    df2 = ampl.get_data('{j in FOOD} 100*Buy[j]/Buy[j].ub')
    # Print them
    print(df2)


if __name__ == '__main__':
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
