#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL, DataFrame
    import amplpy
    from time import time
    os.chdir(os.path.dirname(__file__) or os.curdir)
    try:
        ampl = AMPL()
        ampl.setOption('reset_initial_guesses', True)
        ampl.setOption('send_statuses', False)
        ampl.setOption('relax_integrality', True)

        if argc > 1:
            ampl.setOption('solver', argv[1])

        # Load the AMPL model from file
        modelDirectory = argv[2] if argc == 3 else os.path.join('..', 'models')
        ampl.read(os.path.join(modelDirectory, 'qpmv/qpmv.mod'))
        ampl.read(os.path.join(modelDirectory, 'qpmv/qpmvbit.run'))

        # Set tables directory (parameter used in the script above)
        ampl.getParameter('data_dir').set(os.path.join(modelDirectory, 'qpmv'))
        # Read tables
        ampl.readTable('assetstable')
        ampl.readTable('astrets')

        # Set the output handler to accumulate the output messages
        class MyOutputHandler(amplpy.OutputHandler):
            """
            Class used as an output handler. It only prints the solver output.
            Must implement :class:`amplpy.OutputHandler`.
            """
            def output(self, kind, msg):
                if kind == amplpy.Kind.SOLVE:
                    assert ampl.isBusy()
                    print('Solver: {}'.format(msg))

        class MyErrorHandler(amplpy.ErrorHandler):
            def error(self, exception):
                print('Error:', exception.getMessage())

            def warning(self, exception):
                print('Warning:', exception.getMessage())

        # Create an output handler
        outputHandler = MyOutputHandler()
        ampl.setOutputHandler(outputHandler)

        # Create an error handler
        errorHandler = MyErrorHandler()
        ampl.setErrorHandler(errorHandler)

        print("Main thread: Model setup complete. Solve on worker thread.")
        # Initiate the solution process asynchronously
        ampl.solveAsync()

        # Wait for the solution to complete
        print("Main thread: Waiting for solution to end...")
        start = time()

        # Wait for the async operation to finish
        ampl.wait()
        duration = time() - start

        print("Main thread: done waiting.")
        print("Main thread: waited for {} s".format(duration))

        # Print the objective value
        print("Main thread: cost: {}".format(ampl.getValue('cst')))
    except Exception as e:
        print(e, type(e))
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
