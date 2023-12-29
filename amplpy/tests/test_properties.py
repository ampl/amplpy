#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from . import TestBase


class TestProperties(TestBase.TestBase):
    """Test Properties."""

    def test_var_prop(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.var["x"] = 10

        self.assertEqual(ampl.var["x"].value(), 10)
        self.assertEqual(ampl.get_variable("x").value(), 10)
        self.assertEqual(len(list(ampl.var)), 1)
        self.assertEqual(len(list(ampl.get_variables())), 1)

    def test_con_prop(self):
        ampl = self.ampl
        ampl.eval("var x; s.t. c: x = 10;")
        ampl.con["c"].set_dual(1)  # FIXME: does not seem to have any effect
        self.assertEqual(ampl.con["c"].body(), 10)
        self.assertEqual(ampl.get_constraint("c").body(), 10)
        self.assertEqual(len(list(ampl.con)), 1)
        self.assertEqual(len(list(ampl.get_constraints())), 1)

    def test_obj_prop(self):
        ampl = self.ampl
        ampl.eval("var x; maximize obj: x;")
        self.assertEqual(ampl.obj["obj"].name(), "obj")
        self.assertEqual(ampl.get_objective("obj").name(), "obj")
        self.assertEqual(len(list(ampl.obj)), 1)
        self.assertEqual(len(list(ampl.get_objectives())), 1)

    def test_set_prop(self):
        ampl = self.ampl
        ampl.eval("set s;")
        ampl.set["s"] = [1, 2, 3]
        self.assertEqual(ampl.set["s"].name(), "s")
        self.assertEqual(ampl.get_set("s").name(), "s")
        self.assertEqual(ampl.set["s"].size(), 3)
        self.assertEqual(len(list(ampl.set)), 1)
        self.assertEqual(len(list(ampl.get_sets())), 1)

    def test_param_prop(self):
        ampl = self.ampl
        ampl.eval("param p1; param p2{1..2};")
        self.assertEqual(ampl.param["p1"].name(), "p1")
        self.assertEqual(ampl.get_parameter("p1").name(), "p1")
        ampl.param["p1"] = 3
        self.assertEqual(ampl.param["p1"].value(), 3)
        ampl.param["p2"] = {1: 10, 2: 20}
        self.assertEqual(ampl.param["p2"][1], 10)
        self.assertEqual(ampl.param["p2"][2], 20)
        self.assertEqual(len(list(ampl.param)), 2)
        self.assertEqual(len(list(ampl.get_parameters())), 2)

    def test_option_prop(self):
        ampl = self.ampl
        ampl.option["solver"] = "gurobi"
        self.assertEqual(ampl.option["solver"], "gurobi")
        self.assertEqual(ampl.get_option("solver"), "gurobi")

    def test_solve_result(self):
        ampl = self.ampl
        self.assertEqual(ampl.solve_result, "?")
        self.assertEqual(ampl.solve_result_num, -1)
        ampl.solve()
        self.assertEqual(ampl.solve_result, "solved")
        self.assertEqual(ampl.solve_result_num, 0)


if __name__ == "__main__":
    unittest.main()
