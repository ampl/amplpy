#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL

    os.chdir(os.path.dirname(__file__) or os.curdir)

    # Create an AMPL instance
    ampl = AMPL()

    """
    # If the AMPL installation directory is not in the system search path:
    from amplpy import Environment
    ampl = AMPL(
        Environment('full path to the AMPL installation directory'))
    """

    # Get the value of the option presolve and print
    presolve = ampl.get_option("presolve")
    print("AMPL presolve is", presolve)

    # Set the value to false (maps to 0)
    ampl.set_option("presolve", False)

    # Get the value of the option presolve and print
    presolve = ampl.get_option("presolve")
    print("AMPL presolve is now", presolve)

    # Check whether an option with a specified name
    # exists
    value = ampl.get_option("solver")
    if value is not None:
        print("Option solver exists and has value:", value)

    # Check again, this time failing
    value = ampl.get_option("s_o_l_v_e_r")
    if value is None:
        print("Option s_o_l_v_e_r does not exist!")


if __name__ == "__main__":
    try:
        main(len(sys.argv), sys.argv)
    except Exception as e:
        print(e)
        raise
