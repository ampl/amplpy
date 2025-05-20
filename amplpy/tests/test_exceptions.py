#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from . import TestBase
import amplpy

class TestExceptions(TestBase.TestBase):
    """Test Exceptions."""

    def test_get_option_fail(self):
        ampl = self.ampl
        with self.assertRaises(ValueError):
            ampl.get_option("option 42 42")

    def test_get_value_fail(self):
        ampl = self.ampl
        with self.assertRaises(TypeError):
            ampl.get_value("x.val")

    def test_ampl_couldnotstarted(self):
        env = amplpy.Environment("nodir", "noname")
        with self.assertRaises(RuntimeError):
            ampl = amplpy.AMPL(env)

    def test_export_model_exception(self):
        ampl = self.ampl
        with self.assertRaises(IOError):
            ampl.export_model("///noname")

    def test_export_data_exception(self):
        ampl = self.ampl
        with self.assertRaises(IOError):
            ampl.export_data("///noname")

    def test_snapshot_exception(self):
        ampl = self.ampl
        with self.assertRaises(IOError):
            ampl.snapshot("///noname")

    def test_ampl_cd_exception(self):
        ampl = self.ampl
        with self.assertRaises(RuntimeError):
            ampl.cd("///noname")

    def test_get_variable_exception(self):
        ampl = self.ampl
        ampl.eval("param x;")
        with self.assertRaises(KeyError):
            ampl.get_variable("x")

    def test_get_constraint_exception(self):
        ampl = self.ampl
        ampl.eval("var x;")
        with self.assertRaises(KeyError):
            ampl.get_constraint("x")

    def test_get_objective_exception(self):
        ampl = self.ampl
        ampl.eval("var x;")
        with self.assertRaises(KeyError):
            ampl.get_objective("x")

    def test_get_set_exception(self):
        ampl = self.ampl
        ampl.eval("var x;")
        with self.assertRaises(KeyError):
            ampl.get_set("x")

    def test_get_param_exception(self):
        ampl = self.ampl
        ampl.eval("set x;")
        with self.assertRaises(KeyError):
            ampl.get_parameter("x")

    def test_ampl_exception_methods(self):
        exc = amplpy.AMPLException("test.mod", 42, 5, "Invalid expression")

        self.assertEqual(exc.get_source_name(), "test.mod")
        self.assertEqual(exc.get_line_number(), 42)
        self.assertEqual(exc.get_offset(), 5)
        self.assertEqual(exc.get_message(), "Invalid expression")

    def test_default_errorhandler_error(self):
        ampl = self.ampl
        with self.assertRaises(amplpy.AMPLException) as context:
            ampl.eval("Y Y;")

    def test_default_errorhandler_warning(self):
        ampl = self.ampl
        with self.assertRaises(amplpy.AMPLException) as context:
            ampl.eval("var x := y; var xx := y; var xy := y;")

        self.assertEqual(context.exception.get_message(), 
            "y is not defined\ncontext:  var x :=  >>> y; <<<  var xx := y; var xy := y;")


if __name__ == "__main__":
    unittest.main()
