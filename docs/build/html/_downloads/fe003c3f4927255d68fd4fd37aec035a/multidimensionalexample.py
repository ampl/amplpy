#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
import sys
import os


def main(argc, argv):
    from amplpy import AMPL, DataFrame
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

        ampl.eval('set CITIES; set LINKS within (CITIES cross CITIES);')
        ampl.eval('param cost {LINKS} >= 0; param capacity {LINKS} >= 0;')
        ampl.eval('data; set CITIES := PITT NE SE BOS EWR BWI ATL MCO;')

        cost = [2.5, 3.5, 1.7, 0.7, 1.3, 1.3, 0.8, 0.2, 2.1]
        capacity = [250, 250, 100, 100, 100, 100, 100, 100, 100]
        LinksFrom = ['PITT', 'PITT', 'NE', 'NE', 'NE', 'SE', 'SE', 'SE', 'SE']
        LinksTo = ['NE', 'SE', 'BOS', 'EWR', 'BWI', 'EWR', 'BWI', 'ATL', 'MCO']

        df = DataFrame(('LINKSFrom', 'LINKSTo'), ('cost', 'capacity'))
        df.setColumn('LINKSFrom', LinksFrom)
        df.setColumn('LINKSTo', LinksTo)
        df.setColumn('cost', cost)
        df.setColumn('capacity', capacity)
        print(df)

        ampl.setData(df, 'LINKS')
    except Exception as e:
        print(e)
        raise


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
