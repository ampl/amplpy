#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
from builtins import sorted

import unittest
import os


class TestEnvironment(unittest.TestCase):
    """Test Environment."""

    def test_environment_initialization(self):
        from amplpy import Environment

        env = Environment("binary_directory")
        self.assertEqual("binary_directory", env.get_bin_dir())
        env = Environment("binary_directory", "binary_name")
        self.assertEqual("binary_directory", env.get_bin_dir())
        self.assertEqual("binary_name", env.get_bin_name())
        env.set_bin_dir("binary_directory_2")
        self.assertEqual("binary_directory_2", env.get_bin_dir())
        env.set_bin_name("binary_name_2")
        self.assertEqual("binary_name_2", env.get_bin_name())

    def test_environment(self):
        from amplpy import Environment, AMPL

        env1 = Environment()
        env2 = Environment(os.curdir)
        self.assertEqual(env2.get_bin_dir(), os.curdir)
        env1.set_bin_dir(env2.get_bin_dir())
        self.assertEqual(env1.get_bin_dir(), env1.get_bin_dir())
        self.assertEqual(len(dict(env1)), len(list(env1)))
        self.assertEqual(list(sorted(dict(env1).items())), list(sorted(env1)))
        env1["MyEnvVar"] = "TEST"
        self.assertEqual(env1["MyEnvVar"], "TEST")
        self.assertEqual(env2["MyEnvVar"], None)
        d = dict(env1)
        self.assertEqual(d["MyEnvVar"], "TEST")
        ampl = AMPL(Environment())
        ampl.close()


if __name__ == "__main__":
    unittest.main()
