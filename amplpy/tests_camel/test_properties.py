#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import TestBase
import unittest
import amplpy


class TestProperties(TestBase.TestBase):
    """Test Properties."""

    def testVarProp(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.var["x"] = 10
        self.assertEqual(ampl.var["x"].value(), ampl.getVariable("x").value())
        self.assertEqual(len(list(ampl.var)), len(list(ampl.getVariables())))

    def testConProp(self):
        ampl = self.ampl
        ampl.eval("var x; s.t. c: x = 10;")
        ampl.con["c"] = 10
        self.assertEqual(ampl.con["c"].dual(), ampl.getConstraint("c").dual())
        self.assertEqual(len(list(ampl.con)), len(list(ampl.getConstraints())))

    def testObjProp(self):
        ampl = self.ampl
        ampl.eval("var x; maximize obj: x;")
        self.assertEqual(ampl.obj["obj"].name(), ampl.getObjective("obj").name())
        self.assertEqual(len(list(ampl.obj)), len(list(ampl.getObjectives())))

    def testSetProp(self):
        ampl = self.ampl
        ampl.eval("set s;")
        ampl.set["s"] = [1, 2, 3]
        self.assertEqual(ampl.set["s"].name(), ampl.getSet("s").name())
        self.assertEqual(ampl.set["s"].size(), 3)
        self.assertEqual(len(list(ampl.set)), len(list(ampl.getSets())))

    def testParamProp(self):
        ampl = self.ampl
        ampl.eval("param p1; param p2{1..2};")
        self.assertEqual(ampl.param["p1"].name(), ampl.getParameter("p1").name())
        ampl.param["p1"] = 3
        self.assertEqual(ampl.param["p1"].value(), 3)
        ampl.param["p2"] = {1: 10, 2: 20}
        self.assertEqual(ampl.param["p2"][1], 10)
        self.assertEqual(ampl.param["p2"][2], 20)
        self.assertEqual(len(list(ampl.param)), len(list(ampl.getParameters())))

    def testOptionProp(self):
        ampl = self.ampl
        ampl.option["solver"] = "gurobi"
        self.assertEqual(ampl.option["solver"], ampl.getOption("solver"))


if __name__ == "__main__":
    unittest.main()
