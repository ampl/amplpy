#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from . import TestBase
import amplpy

class TestExceptions(TestBase.TestBase):
    """Test Exceptions."""

    def test_default_errorhandler_error(self):
        ampl = self.ampl
        with self.assertRaises(amplpy.AMPLException):
            ampl.eval("Y Y;")

    def test_default_errorhandler_warning(self):
        ampl = self.ampl
        with self.assertRaises(amplpy.AMPLException) as context:
            ampl.eval("var x := y; var xx := y; var xy := y;")

        self.assertEqual(str(context.exception.get_message()), 
            "y is not defined\ncontext:  var x :=  >>> y; <<<  var xx := y; var xy := y;")


if __name__ == "__main__":
    unittest.main()
