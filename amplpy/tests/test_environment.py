#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

import unittest
import amplpy
import os


class TestEnvironment(unittest.TestCase):
    """Test Environment."""

    def testEnvironment(self):
        from amplpy import Environment, AMPL
        env1 = Environment()
        env2 = Environment(os.curdir)
        self.assertEqual(env2.getBinDir(), os.curdir)
        env1.setBinDir(env2.getBinDir())
        self.assertEqual(env1.getBinDir(), env1.getBinDir())
        self.assertEqual(len(dict(env1)), len(list(env1)))
        self.assertEqual(list(sorted(dict(env1).items())), list(sorted(env1)))
        env1['MyEnvVar'] = 'TEST'
        self.assertEqual(env1['MyEnvVar'], 'TEST')
        self.assertEqual(env2['MyEnvVar'], None)
        d = dict(env1)
        self.assertEqual(d['MyEnvVar'], 'TEST')
        ampl = AMPL(Environment())
        ampl.close()


if __name__ == '__main__':
    unittest.main()
