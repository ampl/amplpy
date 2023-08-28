#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os


def main(argc, argv):
    # You can install amplpy with "python -m pip install amplpy"
    from amplpy import AMPL

    os.chdir(os.path.dirname(__file__) or os.curdir)
    model_directory = os.path.join(os.curdir, "models", "locationtransportation")

    """
    # If you are not using amplpy.modules, and the AMPL installation directory
    # is not in the system search path, add it as follows:
    from amplpy import add_to_path
    add_to_path(r"full path to the AMPL installation directory")
    """

    # Create an AMPL instance
    ampl = AMPL()

    # Must be solved with a solver supporting the suffix dunbdd
    ampl.set_option("solver", "cplex")
    ampl.set_option("presolve", False)
    ampl.set_option("omit_zero_rows", False)

    # Load the AMPL model from file
    ampl.read(os.path.join(model_directory, "trnloc2.mod"))
    # Read data
    ampl.read_data(os.path.join(model_directory, "trnloc.dat"))

    # Get references to AMPL's model entities for easy access.
    ship_cost = ampl.get_objective("Ship_Cost")
    max_ship_cost = ampl.get_variable("Max_Ship_Cost")
    build_var = ampl.get_variable("Build")
    supply = ampl.get_constraint("Supply")
    demand = ampl.get_constraint("Demand")
    num_cut_param = ampl.get_parameter("nCUT")
    cut_type = ampl.get_parameter("cut_type")
    build_param = ampl.get_parameter("build")
    supply_price = ampl.get_parameter("supply_price")
    demand_price = ampl.get_parameter("demand_price")

    num_cut_param.set(0)
    max_ship_cost.set_value(0)
    build_param.set_values([1] * ampl.get_set("ORIG").size())

    num_cuts = 0
    while True:
        num_cuts += 1
        print(f"Iteration {num_cuts}")
        ampl.display("build")
        # Solve the subproblem.
        ampl.solve("Sub")
        result = ship_cost.result()
        if result == "infeasible":
            # Add a feasibility cut.
            num_cut_param.set(num_cuts)
            cut_type.set(num_cuts, "ray")
            for index, value in supply.get_values(["dunbdd"]):
                supply_price[index, num_cuts] = value
            for index, value in demand.get_values(["dunbdd"]):
                demand_price[index, num_cuts] = value
        elif ship_cost.value() > max_ship_cost.value() + 0.00001:
            # Add an optimality cut.
            num_cut_param.set(num_cuts)
            cut_type.set(num_cuts, "point")
            ampl.set_option("display_1col", 0)
            ampl.display("Ship")
            for index, value in supply.get_values():
                supply_price[index, num_cuts] = value
            for index, value in demand.get_values():
                demand_price[index, num_cuts] = value
        else:
            break
        # Re-solve the master problem.
        print("RE-SOLVING MASTER PROBLEM")
        ampl.solve("Master")
        if ampl.solve_result != "solved":
            raise Exception(f"Failed to solve (solve_result: {ampl.solve_result})")
        # Copy the data from the Build variable used in the master problem
        # to the build parameter used in the subproblem.
        build_param.set_values(build_var.get_values())
    print(f"\nProcedure completed in {num_cuts} iterations\n")
    ampl.display("Ship")


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
