#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import pandas as pd


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL

    os.chdir(os.path.dirname(__file__) or os.curdir)

    """
    # If the AMPL installation directory is not in the system search path:
    from amplpy import add_to_path
    add_to_path(r"full path to the AMPL installation directory")

    # Alternatively, load modules if you are using amplpy.modules:
    from amplpy import modules
    modules.load()
    """

    # Create an AMPL instance
    ampl = AMPL()

    if argc > 1:
        ampl.set_option("solver", argv[1])

    # Read the model file
    model_directory = argv[2] if argc == 3 else os.path.join("..", "models")
    ampl.read(os.path.join(model_directory, "diet/diet.mod"))

    # Create a pandas dataframe with data for cost, f_min, f_max
    foods = ["BEEF", "CHK", "FISH", "HAM", "MCH", "MTL", "SPG", "TUR"]
    costs = [3.59, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49]
    fmin = [2, 2, 2, 2, 2, 2, 2, 2]
    fmax = [10, 10, 10, 10, 10, 10, 10, 10]

    df = pd.DataFrame(
        list(zip(foods, costs, fmin, fmax)),
        columns=["FOOD", "cost", "f_min", "f_max"],
    ).set_index("FOOD")

    # Send the data to AMPL and initialize the indexing set "FOOD"
    ampl.set_data(df, "FOOD")

    # Create a pandas dataframe with data for n_min, n_max
    nutrients = ["A", "C", "B1", "B2", "NA", "CAL"]
    nmin = [700, 700, 700, 700, 0, 16000]
    nmax = [20000, 20000, 20000, 20000, 50000, 24000]

    df = pd.DataFrame(
        list(zip(nutrients, nmin, nmax)),
        columns=["NUTR", "n_min", "n_max"],
    ).set_index("NUTR")

    # Send the data to AMPL and initialize the indexing set "NUTR"
    ampl.set_data(df, "NUTR")

    amounts = [
        [60, 8, 8, 40, 15, 70, 25, 60],
        [20, 0, 10, 40, 35, 30, 50, 20],
        [10, 20, 15, 35, 15, 15, 25, 15],
        [15, 20, 10, 10, 15, 15, 15, 10],
        [928, 2180, 945, 278, 1182, 896, 1329, 1397],
        [295, 770, 440, 430, 315, 400, 379, 450],
    ]

    # Set the values for the parameter "amt"
    ampl.param["amt"] = {
        (nutrient, food): amounts[i][j]
        for i, nutrient in enumerate(nutrients)
        for j, food in enumerate(foods)
    }

    # Solve the problem
    ampl.solve()

    # Check if the problem was solved successfully
    solve_result = ampl.get_value("solve_result")
    if solve_result != "solved":
        raise Exception("Failed to solve (solve_result: {})".format(solve_result))

    print("Objective: {}".format(ampl.obj["Total_Cost"].value()))


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
