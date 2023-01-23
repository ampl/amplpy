#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL

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

    if argc > 1:
        ampl.set_option("solver", argv[1])

    # Read the model and data files.
    model_directory = argv[2] if argc == 3 else os.path.join("..", "models")
    ampl.read(os.path.join(model_directory, "diet/diet.mod"))
    ampl.read_data(os.path.join(model_directory, "diet/diet.dat"))

    # Solve
    ampl.solve()
    solve_result = ampl.get_value("solve_result")
    if solve_result != "solved":
        raise Exception("Failed to solve (solve_result: {})".format(solve_result))

    # Get objective entity by AMPL name
    totalcost = ampl.get_objective("Total_Cost")
    # Print it
    print("Objective is:", totalcost.value())

    # Reassign data - specific instances
    cost = ampl.get_parameter("cost")
    cost.set_values({"BEEF": 5.01, "HAM": 4.55})
    print("Increased costs of beef and ham.")

    # Resolve and display objective
    ampl.solve()
    solve_result = ampl.get_value("solve_result")
    if solve_result != "solved":
        raise Exception("Failed to solve (solve_result: {})".format(solve_result))
    print("New objective value:", totalcost.value())

    # Reassign data - all instances
    elements = [3, 5, 5, 6, 1, 2, 5.01, 4.55]
    cost.set_values(elements)
    print("Updated all costs.")

    # Resolve and display objective
    ampl.solve()
    solve_result = ampl.get_value("solve_result")
    if solve_result != "solved":
        raise Exception("Failed to solve (solve_result: {})".format(solve_result))
    print("New objective value:", totalcost.value())

    # Get the values of the variable Buy in a dataframe object
    buy = ampl.get_variable("Buy")
    df = buy.get_values()
    # Print as pandas dataframe
    print(df.to_pandas())

    # Get the values of an expression into a DataFrame object
    df2 = ampl.get_data("{j in FOOD} 100*Buy[j]/Buy[j].ub")
    # Print as pandas dataframe
    print(df2.to_pandas())


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
