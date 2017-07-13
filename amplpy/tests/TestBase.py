#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

from .context import amplpy
import unittest


class TestBase(unittest.TestCase):
    def setUp(self):
        self.ampl = amplpy.AMPL()

    def tearDown(self):
        self.ampl.close()


if __name__ == '__main__':
    unittest.main()
