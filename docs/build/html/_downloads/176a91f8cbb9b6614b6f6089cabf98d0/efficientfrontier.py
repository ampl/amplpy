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
        modelDirectory = os.path.join(
            argv[2] if argc == 3 else os.path.join('..', 'models'),
            'qpmv'
        )

        ampl = AMPL()
        # Number of steps of the efficient frontier
        steps = 10

        if argc > 1:
            ampl.setOption('solver', argv[1])

        ampl.setOption('reset_initial_guesses', True)
        ampl.setOption('send_statuses', False)
        ampl.setOption('solver', 'cplex')

        # Load the AMPL model from file
        ampl.read(os.path.join(modelDirectory, 'qpmv.mod'))
        ampl.read(os.path.join(modelDirectory, 'qpmvbit.run'))

        # Set tables directory (parameter used in the script above)
        ampl.getParameter('data_dir').set(modelDirectory)
        # Read tables
        ampl.readTable('assetstable')
        ampl.readTable('astrets')

        portfolioReturn = ampl.getVariable('portret')
        averageReturn = ampl.getParameter('averret')
        targetReturn = ampl.getParameter('targetret')
        variance = ampl.getObjective('cst')

        # Relax the integrality
        ampl.setOption('relax_integrality', True)
        # Solve the problem
        ampl.solve()
        # Calibrate the efficient frontier range
        minret = portfolioReturn.value()
        values = averageReturn.getValues()
        col = values.getColumn('averret')
        maxret = max(col)
        stepsize = (maxret - minret) / steps
        returns = [None] * steps
        variances = [None] * steps
        for i in range(steps):
            print(
                'Solving for return = {:g}'.format(maxret - (i - 1) * stepsize)
            )
            # Set target return to the desired point
            targetReturn.set(maxret - (i - 1) * stepsize)
            ampl.eval('let stockopall:={};let stockrun:=stockall;')
            # Relax integrality
            ampl.setOption('relax_integrality', True)
            ampl.solve()
            print('QP result = {:g}'.format(variance.value()))
            # Adjust included stocks
            ampl.eval('let stockrun:={i in stockrun:weights[i]>0};')
            ampl.eval('let stockopall:={i in stockrun:weights[i]>0.5};')
            # Set integrality back
            ampl.setOption('relax_integrality', False)
            ampl.solve()
            print('QMIP result = {:g}'.format(variance.value()))
            # Store data of corrent frontier point
            returns[i] = maxret - (i - 1) * stepsize
            variances[i] = variance.value()

        # Display efficient frontier points
        print('RETURN    VARIANCE')
        for i in range(steps):
            print('{:-6f}  {:-6f}'.format(returns[i], variances[i]))
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
