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

        # Get the value of the option presolve and print
        presolve = ampl.getOption('presolve')
        print("AMPL presolve is", presolve)

        # Set the value to false (maps to 0)
        ampl.setOption('presolve', False)

        # Get the value of the option presolve and print
        presolve = ampl.getOption('presolve')
        print("AMPL presolve is now", presolve)

        # Check whether an option with a specified name
        # exists
        value = ampl.getOption('solver')
        if value is not None:
            print("Option solver exists and has value:", value)

        # Check again, this time failing
        value = ampl.getOption('s_o_l_v_e_r')
        if value is None:
            print("Option s_o_l_v_e_r does not exist!")
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
