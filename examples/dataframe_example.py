#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
import pandas as pd


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL, DataFrame

    os.chdir(os.path.dirname(__file__) or os.curdir)
    model_directory = os.path.join(os.curdir, "models", "diet")

    # Create first pandas.DataFrame (for data indexed over NUTR)
    nutr_df = pd.DataFrame(
        [
            ("A", 700, 20000),
            ("C", 700, 20000),
            ("B1", 700, 20000),
            ("B2", 700, 20000),
            ("NA", 0, 50000),
            ("CAL", 16000, 24000),
        ],
        columns=["NUTR", "n_min", "n_max"],
    ).set_index("NUTR")

    # Create second pandas.DataFrame (for data indexed over FOOD)
    food_df = pd.DataFrame(
        {
            "FOOD": ["BEEF", "CHK", "FISH", "HAM", "MCH", "MTL", "SPG", "TUR"],
            "f_min": [2] * 8,
            "f_max": [10] * 8,
            "cost": [3.19, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49],
        }
    ).set_index("FOOD")

    # Create third pandas.DataFrame to assign data to the AMPL entity
    # param amt{NUTR, FOOD};
    amt_df = (
        pd.DataFrame(
            np.array(
                [
                    [60, 8, 8, 40, 15, 70, 25, 60],
                    [20, 0, 10, 40, 35, 30, 50, 20],
                    [10, 20, 15, 35, 15, 15, 25, 15],
                    [15, 20, 10, 10, 15, 15, 15, 10],
                    [928, 2180, 945, 278, 1182, 896, 1329, 1397],
                    [295, 770, 440, 430, 315, 400, 379, 450],
                ]
            ),
            columns=food_df.index.to_list(),
            index=nutr_df.index.to_list(),
        )
        .stack()
        .rename("amt")
    )

    # Create an AMPL instance
    ampl = AMPL()

    # Set the solver to use
    solver = argv[1] if argc > 1 else "highs"
    ampl.set_option("solver", solver)

    # Read the model file
    ampl.read(os.path.join(model_directory, "diet.mod"))

    # Assign data to NUTR, n_min and n_max
    ampl.set_data(nutr_df, "NUTR")
    # Assign data to FOOD, f_min, f_max and cost
    ampl.set_data(food_df, "FOOD")

    # Assign data to amt
    ampl.set_data(amt_df)
    # Solve the model

    ampl.solve()

    # Print out the result
    objective_value = ampl.get_objective("Total_Cost").value()
    print(f"Objective function value: {objective_value}")

    # Get the values of the variable Buy in a dataframe
    results = ampl.get_variable("Buy").get_values()
    # Print
    print(results)


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
