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

        modelDirectory = os.path.join(
            argv[2] if argc == 3 else os.path.join('..', 'models'),
            'tracking'
        )

        # Load the AMPL model from file
        ampl.read(os.path.join(modelDirectory, 'tracking.mod'))
        # Read data
        ampl.readData(os.path.join(modelDirectory, 'tracking.dat'))
        # Read table declarations
        ampl.read(os.path.join(modelDirectory, 'trackingbit.run'))
        # Set tables directory (parameter used in the script above)
        ampl.getParameter('data_dir').set(modelDirectory)
        # Read tables
        ampl.readTable('assets')
        ampl.readTable('indret')
        ampl.readTable('returns')

        hold = ampl.getVariable('hold')
        ifinuniverse = ampl.getParameter('ifinuniverse')

        # Relax the integrality
        ampl.setOption('relax_integrality', True)
        # Solve the problem
        ampl.solve()
        objectives = list(obj for name, obj in ampl.getObjectives())
        assert objectives[0].value() == ampl.getObjective('cst').value()
        print("QP objective value", ampl.getObjective('cst').value())

        lowcutoff = 0.04
        highcutoff = 0.1

        # Get the variable representing the (relaxed) solution vector
        holdvalues = hold.getValues()
        toHold = []
        # For each asset, if it was held by more than the highcutoff,
        # forces it in the model, if less than lowcutoff, forces it out
        for value in holdvalues.getColumn('hold'):
            if value < lowcutoff:
                toHold.append(0)
            elif value > highcutoff:
                toHold.append(2)
            else:
                toHold.append(1)
        # uses those values for the parameter ifinuniverse, which controls
        # which
        # stock is included or not in the solution
        ifinuniverse.setValues(toHold)

        # Get back to the integer problem
        ampl.setOption('relax_integrality', False)
        # Solve the (integer) problem
        ampl.solve()
        print("QMIP objective value", ampl.getObjective('cst').value())
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
