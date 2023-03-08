#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL, DataFrame

    os.chdir(os.path.dirname(__file__) or os.curdir)
    model_directory = os.path.join(os.curdir, "models", "diet")

    # Note: If you want to perform data transformations use pandas dataframes.
    # amplpy dataframes are simple dataframes for data communication only.

    # Create first dataframe (for data indexed over NUTR)
    # Add data row by row
    df1 = DataFrame("NUTR", ("n_min", "n_max"))
    df1.add_row("A", 700, 20000)
    df1.add_row("B1", 700, 20000)
    df1.add_row("B2", 700, 20000)
    df1.add_row("C", 700, 20000)
    df1.add_row("CAL", 16000, 24000)
    df1.add_row("NA", 0.0, 50000)

    # Create second dataframe (for data indexed over FOOD)
    # Add column by column
    df2 = DataFrame("FOOD")
    foods = ["BEEF", "CHK", "FISH", "HAM", "MCH", "MTL", "SPG", "TUR"]
    df2.set_column("FOOD", foods)
    contents = [2] * 8
    df2.add_column("f_min", contents)
    contents = [10] * 8
    df2.add_column("f_max", contents)
    costs = [3.19, 2.59, 2.29, 2.89, 1.89, 1.99, 1.99, 2.49]
    df2.add_column("cost", costs)

    # Create third dataframe, to assign data to the AMPL entity
    # param amt{NUTR, FOOD};
    df3 = DataFrame(index=("NUTR", "FOOD"))
    # Populate the set columns
    nutr_with_multiplicity = [""] * 48
    food_with_multiplicity = [""] * 48
    i = 0
    for n in range(6):
        for f in range(8):
            nutr_with_multiplicity[i] = df1.get_row_by_index(n)[0]
            food_with_multiplicity[i] = foods[f]
            i += 1
    df3.set_column("NUTR", nutr_with_multiplicity)
    df3.set_column("FOOD", food_with_multiplicity)

    # Populate with all these values
    values = [
        60,
        8,
        8,
        40,
        15,
        70,
        25,
        60,
        10,
        20,
        15,
        35,
        15,
        15,
        25,
        15,
        15,
        20,
        10,
        10,
        15,
        15,
        15,
        10,
        20,
        0,
        10,
        40,
        35,
        30,
        50,
        20,
        295,
        770,
        440,
        430,
        315,
        400,
        370,
        450,
        968,
        2180,
        945,
        278,
        1182,
        896,
        1329,
        1397,
    ]
    df3.add_column("amt", values)

    # Create an AMPL instance
    ampl = AMPL()

    # Set the solver to use
    solver = argv[1] if argc > 1 else "highs"
    ampl.set_option("solver", solver)

    # Read the model file
    ampl.read(os.path.join(model_directory, "diet.mod"))

    # Assign data to NUTR, n_min and n_max
    ampl.set_data(df1, "NUTR")
    # Assign data to FOOD, f_min, f_max and cost
    ampl.set_data(df2, "FOOD")
    # Assign data to amt
    ampl.set_data(df3)
    # Solve the model
    ampl.solve()

    # Print out the result
    print(
        "Objective function value: {}".format(ampl.get_objective("Total_Cost").value())
    )

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
