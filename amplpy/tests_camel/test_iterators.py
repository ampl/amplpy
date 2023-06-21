#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import TestBase
import unittest
import amplpy


class TestIterators(TestBase.TestBase):
    """Test Iterators."""

    def testSetIterators(self):
        ampl = self.ampl
        ampl.eval("set x;")
        self.assertEqual(len(ampl.getSets()), ampl.getSets().size())
        self.assertEqual(ampl.getSets().size(), len(list(ampl.getSets())))
        self.assertEqual(ampl.getSets().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.getSets().size(), 0)
        ampl.eval("set x;")
        self.assertEqual(ampl.getSets().size(), 1)
        ampl.eval("set y{1..2};")
        self.assertEqual(ampl.getSets().size(), 2)
        ampl.eval('set z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.getSets().size(), 3)
        ampl.eval("set xx{1..2,4..5};")
        self.assertEqual(ampl.getSets().size(), 4)
        ampl.eval("set yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.getSets().size(), 5)
        ampl.eval('set zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.getSets().size(), 6)
        # self.assertEqual(ampl.getSet("x").numInstances(), len(dict(ampl.getSet("x"))))
        self.assertEqual(ampl.getSet("x").numInstances(), 1)
        self.assertEqual(ampl.getSet("y").numInstances(), 2)
        self.assertEqual(ampl.getSet("z").numInstances(), 4)
        self.assertEqual(ampl.getSet("xx").numInstances(), 4)
        self.assertEqual(ampl.getSet("yy").numInstances(), 8)
        self.assertEqual(ampl.getSet("zz").numInstances(), 8)
        self.assertEqual(max(s.numInstances() for name, s in ampl.getSets()), 8)
        self.assertEqual(ampl.getSet("x").name(), ampl.getSets()["x"].name())

    def testParameterIterators(self):
        ampl = self.ampl
        ampl.eval("param x;")
        self.assertEqual(len(ampl.getParameters()), ampl.getParameters().size())
        self.assertEqual(ampl.getParameters().size(), len(list(ampl.getParameters())))
        self.assertEqual(ampl.getParameters().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.getParameters().size(), 0)
        ampl.eval("param x;")
        self.assertEqual(ampl.getParameters().size(), 1)
        ampl.eval("param y{1..2};")
        self.assertEqual(ampl.getParameters().size(), 2)
        ampl.eval('param z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.getParameters().size(), 3)
        ampl.eval("param xx{1..2,4..5};")
        self.assertEqual(ampl.getParameters().size(), 4)
        ampl.eval("param yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.getParameters().size(), 5)
        ampl.eval('param zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.getParameters().size(), 6)
        self.assertEqual(
            ampl.getParameter("x").numInstances(), len(dict(ampl.getParameter("x")))
        )
        self.assertEqual(ampl.getParameter("x").numInstances(), 1)
        self.assertEqual(ampl.getParameter("y").numInstances(), 2)
        self.assertEqual(ampl.getParameter("z").numInstances(), 4)
        self.assertEqual(ampl.getParameter("xx").numInstances(), 4)
        self.assertEqual(ampl.getParameter("yy").numInstances(), 8)
        self.assertEqual(ampl.getParameter("zz").numInstances(), 8)
        self.assertEqual(max(p.numInstances() for name, p in ampl.getParameters()), 8)
        self.assertEqual(
            ampl.getParameter("x").name(), ampl.getParameters()["x"].name()
        )

    def testVariableIterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        self.assertEqual(len(ampl.getVariables()), ampl.getVariables().size())
        self.assertEqual(ampl.getVariables().size(), len(list(ampl.getVariables())))
        self.assertEqual(ampl.getVariables().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.getVariables().size(), 0)
        ampl.eval("var x;")
        self.assertEqual(ampl.getVariables().size(), 1)
        ampl.eval("var y{1..2};")
        self.assertEqual(ampl.getVariables().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.getVariables().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        self.assertEqual(ampl.getVariables().size(), 4)
        ampl.eval("var yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.getVariables().size(), 5)
        ampl.eval('var zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.getVariables().size(), 6)
        self.assertEqual(
            ampl.getVariable("x").numInstances(), len(dict(ampl.getVariable("x")))
        )
        self.assertEqual(ampl.getVariable("x").numInstances(), 1)
        self.assertEqual(ampl.getVariable("y").numInstances(), 2)
        self.assertEqual(ampl.getVariable("z").numInstances(), 4)
        self.assertEqual(ampl.getVariable("xx").numInstances(), 4)
        self.assertEqual(ampl.getVariable("yy").numInstances(), 8)
        self.assertEqual(ampl.getVariable("zz").numInstances(), 8)
        self.assertEqual(
            max(var.numInstances() for name, var in ampl.getVariables()), 8
        )
        self.assertEqual(ampl.getVariable("x").name(), ampl.getVariables()["x"].name())

    def testConstraintIterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.eval("s.t. c_x: x = 0;")
        self.assertEqual(ampl.getConstraints().size(), len(ampl.getConstraints()))
        self.assertEqual(ampl.getConstraints().size(), len(list(ampl.getConstraints())))
        self.assertEqual(ampl.getConstraints().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.getConstraints().size(), 0)
        ampl.eval("var x;")
        ampl.eval("s.t. c_x: x = 0;")
        self.assertEqual(ampl.getConstraints().size(), 1)
        ampl.eval("var y{1..2};")
        ampl.eval("s.t. c_y{i in 1..2}: y[i] = i;")
        self.assertEqual(ampl.getConstraints().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        ampl.eval('s.t. c_z{(i, j) in {1..2, {"a", "b"}}}: z[i,j] = i;')
        self.assertEqual(ampl.getConstraints().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        ampl.eval("s.t. c_xx{(i, j) in {1..2,4..5}}: xx[i,j] = i+j;")
        self.assertEqual(ampl.getConstraints().size(), 4)
        self.assertEqual(
            ampl.getConstraint("c_x").numInstances(),
            len(dict(ampl.getConstraint("c_x"))),
        )
        self.assertEqual(ampl.getConstraint("c_x").numInstances(), 1)
        self.assertEqual(ampl.getConstraint("c_y").numInstances(), 2)
        self.assertEqual(ampl.getConstraint("c_z").numInstances(), 4)
        self.assertEqual(ampl.getConstraint("c_xx").numInstances(), 4)
        self.assertEqual(
            max(con.numInstances() for name, con in ampl.getConstraints()), 4
        )
        self.assertEqual(
            ampl.getConstraint("c_x").name(), ampl.getConstraints()["c_x"].name()
        )

    def testObjectiveIterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.eval("maximize c_x: x;")
        self.assertEqual(ampl.getObjectives().size(), len(ampl.getObjectives()))
        self.assertEqual(ampl.getObjectives().size(), len(list(ampl.getObjectives())))
        self.assertEqual(ampl.getObjectives().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.getObjectives().size(), 0)
        ampl.eval("var x;")
        ampl.eval("maximize c_x: x;")
        self.assertEqual(ampl.getObjectives().size(), 1)
        ampl.eval("var y{1..2};")
        ampl.eval("maximize c_y{i in 1..2}: y[i];")
        self.assertEqual(ampl.getObjectives().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        ampl.eval('maximize c_z{(i, j) in {1..2, {"a", "b"}}}: z[i,j];')
        self.assertEqual(ampl.getObjectives().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        ampl.eval("maximize c_xx{(i, j) in {1..2,4..5}}: xx[i,j];")
        self.assertEqual(ampl.getObjectives().size(), 4)
        self.assertEqual(
            ampl.getObjective("c_x").numInstances(), len(dict(ampl.getObjective("c_x")))
        )
        self.assertEqual(ampl.getObjective("c_x").numInstances(), 1)
        self.assertEqual(ampl.getObjective("c_y").numInstances(), 2)
        self.assertEqual(ampl.getObjective("c_z").numInstances(), 4)
        self.assertEqual(ampl.getObjective("c_xx").numInstances(), 4)
        self.assertEqual(
            max(obj.numInstances() for name, obj in ampl.getObjectives()), 4
        )
        self.assertEqual(
            ampl.getObjective("c_x").name(), ampl.getObjectives()["c_x"].name()
        )


if __name__ == "__main__":
    unittest.main()
