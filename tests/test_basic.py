# -*- coding: utf-8 -*-

from .context import amplpy
import TestBase
import unittest


class BasicTestSuite(TestBase.TestBase):
    """Basic test cases."""

    def testEval(self):
        self.ampl.eval("option version;")


if __name__ == '__main__':
    unittest.main()
