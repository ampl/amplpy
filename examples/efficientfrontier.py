#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL
    os.chdir(os.path.dirname(__file__) or os.curdir)
    model_directory = os.path.join(
        argv[2] if argc == 3 else os.path.join('..', 'models'),
        'qpmv'
    )

    # Create an AMPL instance
    ampl = AMPL()

    '''
    # If the AMPL installation directory is not in the system search path:
    from amplpy import Environment
    ampl = AMPL(
        Environment('full path to the AMPL installation directory'))
    '''

    # Number of steps of the efficient frontier
    steps = 10

    if argc > 1:
        ampl.set_option('solver', argv[1])

    ampl.set_option('reset_initial_guesses', True)
    ampl.set_option('send_statuses', False)
    ampl.set_option('solver', 'cplex')

    # Load the AMPL model from file
    ampl.read(os.path.join(model_directory, 'qpmv.mod'))
    ampl.read(os.path.join(model_directory, 'qpmvbit.run'))

    # Set tables directory (parameter used in the script above)
    ampl.get_parameter('data_dir').set(model_directory)
    # Read tables
    ampl.read_table('assetstable')
    ampl.read_table('astrets')

    portfolio_return = ampl.getVariable('portret')
    average_return = ampl.get_parameter('averret')
    target_return = ampl.get_parameter('targetret')
    variance = ampl.get_objective('cst')

    # Relax the integrality
    ampl.set_option('relax_integrality', True)
    # Solve the problem
    ampl.solve()
    # Calibrate the efficient frontier range
    minret = portfolio_return.value()
    values = average_return.get_values()
    col = values.get_column('averret')
    maxret = max(col)
    stepsize = (maxret - minret) / steps
    returns = [None] * steps
    variances = [None] * steps
    for i in range(steps):
        print(
            'Solving for return = {:g}'.format(maxret - (i - 1) * stepsize)
        )
        # Set target return to the desired point
        target_return.set(maxret - (i - 1) * stepsize)
        ampl.eval('let stockopall:={};let stockrun:=stockall;')
        # Relax integrality
        ampl.set_option('relax_integrality', True)
        ampl.solve()
        print('QP result = {:g}'.format(variance.value()))
        # Adjust included stocks
        ampl.eval('let stockrun:={i in stockrun:weights[i]>0};')
        ampl.eval('let stockopall:={i in stockrun:weights[i]>0.5};')
        # Set integrality back
        ampl.set_option('relax_integrality', False)
        ampl.solve()
        print('QMIP result = {:g}'.format(variance.value()))
        # Store data of corrent frontier point
        returns[i] = maxret - (i - 1) * stepsize
        variances[i] = variance.value()

    # Display efficient frontier points
    print('RETURN    VARIANCE')
    for i in range(steps):
        print('{:-6f}  {:-6f}'.format(returns[i], variances[i]))


if __name__ == '__main__':
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
