#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import amplpy
import os


class TestEnvironment(unittest.TestCase):
    """Test Environment."""

    def testEnvironmentInitialization(self):
        from amplpy import Environment

        env = Environment("binary_directory")
        self.assertEqual("binary_directory", env.getBinDir())
        env = Environment("binary_directory", "binary_name")
        self.assertEqual("binary_directory", env.getBinDir())
        self.assertEqual("binary_name", env.getBinName())
        env.setBinDir("binary_directory_2")
        self.assertEqual("binary_directory_2", env.getBinDir())
        env.setBinName("binary_name_2")
        self.assertEqual("binary_name_2", env.getBinName())

    def testEnvironment(self):
        from amplpy import Environment, AMPL

        env1 = Environment()
        env2 = Environment(os.curdir)
        self.assertEqual(env2.getBinDir(), os.curdir)
        env1.setBinDir(env2.getBinDir())
        self.assertEqual(env1.getBinDir(), env1.getBinDir())
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
