#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL
    import amplpy
    from time import time

    os.chdir(os.path.dirname(__file__) or os.curdir)

    """
    # If the AMPL installation directory is not in the system search path:
    from amplpy import add_to_path
    add_to_path(r"full path to the AMPL installation directory")

    # Alternatively, load modules if you are using amplpy.modules:
    from amplpy import tools
    tools.modules.load()
    """

    # Create an AMPL instance
    ampl = AMPL()

    ampl.set_option("reset_initial_guesses", True)
    ampl.set_option("send_statuses", False)
    ampl.set_option("relax_integrality", True)
    if argc > 1:
        ampl.set_option("solver", argv[1])

    # Load the AMPL model from file
    model_directory = argv[2] if argc == 3 else os.path.join("..", "models")
    ampl.read(os.path.join(model_directory, "qpmv/qpmv.mod"))
    ampl.read(os.path.join(model_directory, "qpmv/qpmvbit.run"))

    # Set tables directory (parameter used in the script above)
    ampl.get_parameter("data_dir").set(os.path.join(model_directory, "qpmv"))
    # Read tables
    ampl.read_table("assetstable")
    ampl.read_table("astrets")

    # Set the output handler to accumulate the output messages
    class MyOutputHandler(amplpy.OutputHandler):
        """
        Class used as an output handler. It only prints the solver output.
        Must implement :class:`amplpy.OutputHandler`.
        """

        def output(self, kind, msg):
            if kind == amplpy.Kind.SOLVE:
                assert ampl.is_busy()
                print("Solver: {}".format(msg))

    class MyErrorHandler(amplpy.ErrorHandler):
        def error(self, exception):
            print("Error:", exception.get_message())

        def warning(self, exception):
            print("Warning:", exception.get_message())

    # Create an output handler
    output_handler = MyOutputHandler()
    ampl.set_output_handler(output_handler)

    # Create an error handler
    error_handler = MyErrorHandler()
    ampl.set_error_handler(error_handler)

    print("Main thread: Model setup complete. Solve on worker thread.")
    # Initiate the solution process asynchronously
    ampl.solve_async()

    # Wait for the solution to complete
    print("Main thread: Waiting for solution to end...")
    start = time()

    # Wait for the async operation to finish
    ampl.wait()
    duration = time() - start

    print("Main thread: done waiting.")
    print("Main thread: waited for {} s".format(duration))

    # Print the objective value
    print("Main thread: cost: {}".format(ampl.get_value("cst")))


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
