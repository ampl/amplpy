#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted

import unittest
from . import TestBase


class TestProperties(TestBase.TestBase):
    """Test Properties."""

    def test_var_prop(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.var["x"] = 10
        self.assertEqual(ampl.var["x"].value(), ampl.get_variable("x").value())
        self.assertEqual(len(list(ampl.var)), len(list(ampl.get_variables())))

    def test_con_prop(self):
        ampl = self.ampl
        ampl.eval("var x; s.t. c: x = 10;")
        ampl.con["c"] = 10
        self.assertEqual(ampl.con["c"].dual(), ampl.get_constraint("c").dual())
        self.assertEqual(len(list(ampl.con)), len(list(ampl.get_constraints())))

    def test_obj_prop(self):
        ampl = self.ampl
        ampl.eval("var x; maximize obj: x;")
        self.assertEqual(ampl.obj["obj"].name(), ampl.get_objective("obj").name())
        self.assertEqual(len(list(ampl.obj)), len(list(ampl.get_objectives())))

    def test_set_prop(self):
        ampl = self.ampl
        ampl.eval("set s;")
        ampl.set["s"] = [1, 2, 3]
        self.assertEqual(ampl.set["s"].name(), ampl.get_set("s").name())
        self.assertEqual(ampl.set["s"].size(), 3)
        self.assertEqual(len(list(ampl.set)), len(list(ampl.get_sets())))

    def test_param_prop(self):
        ampl = self.ampl
        ampl.eval("param p1; param p2{1..2};")
        self.assertEqual(ampl.param["p1"].name(), ampl.get_parameter("p1").name())
        ampl.param["p1"] = 3
        self.assertEqual(ampl.param["p1"].value(), 3)
        ampl.param["p2"] = {1: 10, 2: 20}
        self.assertEqual(ampl.param["p2"][1], 10)
        self.assertEqual(ampl.param["p2"][2], 20)
        self.assertEqual(len(list(ampl.param)), len(list(ampl.get_parameters())))

    def test_option_prop(self):
        ampl = self.ampl
        ampl.option["solver"] = "gurobi"
        self.assertEqual(ampl.option["solver"], ampl.get_option("solver"))


if __name__ == "__main__":
    unittest.main()
