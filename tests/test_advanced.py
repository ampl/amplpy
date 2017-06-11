# -*- coding: utf-8 -*-

from .context import amplpy
import TestBase
import unittest


class AdvancedTestSuite(TestBase.TestBase):
    """Advanced test cases."""

    def testEnvironment(self):
        e = amplpy.Environment()


if __name__ == '__main__':
    unittest.main()
