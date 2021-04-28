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
        # Create an AMPL instance
        ampl = AMPL()

        """
        # If the AMPL installation directory is not in the system search path:
        from amplpy import Environment
        ampl = AMPL(
            Environment('full path to the AMPL installation directory'))
        """

        if argc > 1:
            # ampl.setOption('solver', argv[1])
            pass

        # Must be solved with a solver supporting the suffix dunbdd
        ampl.setOption('solver', 'cplex')
        ampl.setOption('presolve', False)
        ampl.setOption('omit_zero_rows', False)
        ampl._startRecording('interactions.log')

        modelDirectory = os.path.join(
            argv[2] if argc == 3 else os.path.join('..', 'models'),
            'locationtransportation'
        )

        # Load the AMPL model from file
        ampl.read(os.path.join(modelDirectory, 'trnloc2.mod'))
        # Read data
        ampl.readData(os.path.join(modelDirectory, 'trnloc.dat'))

        # Get references to AMPL's model entities for easy access.
        shipCost = ampl.getObjective('Ship_Cost')
        maxShipCost = ampl.getVariable('Max_Ship_Cost')
        buildVar = ampl.getVariable('Build')
        supply = ampl.getConstraint('Supply')
        demand = ampl.getConstraint('Demand')
        numCutParam = ampl.getParameter('nCUT')
        cutType = ampl.getParameter('cut_type')
        buildParam = ampl.getParameter('build')
        supplyPrice = ampl.getParameter('supply_price')
        demandPrice = ampl.getParameter('demand_price')

        numCutParam.set(0)
        maxShipCost.setValue(0)
        buildParam.setValues([1] * ampl.getSet('ORIG').size())

        numCuts = 0
        while True:
            numCuts += 1
            print('Iteration {}'.format(numCuts))
            ampl.display('build')
            # Solve the subproblem.
            ampl.eval('solve Sub;')
            result = shipCost.result()
            if result.find('infeasible') != -1:
                # Add a feasibility cut.
                numCutParam.set(numCuts)
                cutType.set(numCuts, 'ray')
                for index, value in supply.getValues(['dunbdd']):
                    supplyPrice[index, numCuts] = value
                for index, value in demand.getValues(['dunbdd']):
                    demandPrice[index, numCuts] = value
            elif shipCost.value() > maxShipCost.value() + 0.00001:
                # Add an optimality cut.
                numCutParam.set(numCuts)
                cutType.set(numCuts, 'point')
                ampl.setOption('display_1col', 0)
                ampl.display('Ship')
                for index, value in supply.getValues():
                    supplyPrice[index, numCuts] = value
                for index, value in demand.getValues():
                    demandPrice[index, numCuts] = value
            else:
                break
            # Re-solve the master problem.
            print('RE-SOLVING MASTER PROBLEM')
            ampl.eval('solve Master;')
            # Copy the data from the Build variable used in the master problem
            # to the build parameter used in the subproblem.
            buildParam.setValues(buildVar.getValues())
        print('\nProcedure completed in {} iterations\n'.format(numCuts))
        ampl.display('Ship')
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
