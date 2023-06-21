#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from . import TestBase


class TestIterators(TestBase.TestBase):
    """Test Iterators."""

    def test_set_iterators(self):
        ampl = self.ampl
        ampl.eval("set x;")
        self.assertEqual(len(ampl.get_sets()), ampl.get_sets().size())
        self.assertEqual(ampl.get_sets().size(), len(list(ampl.get_sets())))
        self.assertEqual(ampl.get_sets().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.get_sets().size(), 0)
        ampl.eval("set x;")
        self.assertEqual(ampl.get_sets().size(), 1)
        ampl.eval("set y{1..2};")
        self.assertEqual(ampl.get_sets().size(), 2)
        ampl.eval('set z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.get_sets().size(), 3)
        ampl.eval("set xx{1..2,4..5};")
        self.assertEqual(ampl.get_sets().size(), 4)
        ampl.eval("set yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.get_sets().size(), 5)
        ampl.eval('set zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.get_sets().size(), 6)
        self.assertEqual(list(ampl.get_set("x").members()), list(ampl.get_set("x")))
        self.assertEqual(ampl.get_set("x").num_instances(), 1)
        self.assertEqual(ampl.get_set("y").num_instances(), 2)
        self.assertEqual(list(ampl.set["y"][1].members()), list(ampl.set["y"][1]))
        self.assertEqual(ampl.get_set("z").num_instances(), 4)
        self.assertEqual(
            list(ampl.set["z"][1, "a"].members()), list(ampl.set["z"][1, "a"])
        )
        self.assertEqual(ampl.get_set("xx").num_instances(), 4)
        self.assertEqual(
            list(ampl.set["xx"][1, 4].members()), list(ampl.set["xx"][1, 4])
        )
        self.assertEqual(ampl.get_set("yy").num_instances(), 8)
        self.assertEqual(
            list(ampl.set["yy"][1, 4, 7].members()), list(ampl.set["yy"][1, 4, 7])
        )
        self.assertEqual(ampl.get_set("zz").num_instances(), 8)
        self.assertEqual(
            list(ampl.set["zz"][1, "a", 5].members()), list(ampl.set["zz"][1, "a", 5])
        )
        self.assertEqual(max(s.num_instances() for name, s in ampl.get_sets()), 8)
        self.assertEqual(ampl.get_set("x").name(), ampl.get_sets()["x"].name())
        with self.assertRaises(KeyError):
            ampl.get_set("notfound")
        with self.assertRaises(KeyError):
            ampl.get_sets()["notfound"]

    def test_parameter_iterators(self):
        ampl = self.ampl
        ampl.eval("param x;")
        self.assertEqual(len(ampl.get_parameters()), ampl.get_parameters().size())
        self.assertEqual(ampl.get_parameters().size(), len(list(ampl.get_parameters())))
        self.assertEqual(ampl.get_parameters().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.get_parameters().size(), 0)
        ampl.eval("param x;")
        self.assertEqual(ampl.get_parameters().size(), 1)
        ampl.eval("param y{1..2};")
        self.assertEqual(ampl.get_parameters().size(), 2)
        ampl.eval('param z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.get_parameters().size(), 3)
        ampl.eval("param xx{1..2,4..5};")
        self.assertEqual(ampl.get_parameters().size(), 4)
        ampl.eval("param yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.get_parameters().size(), 5)
        ampl.eval('param zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.get_parameters().size(), 6)
        self.assertEqual(
            ampl.get_parameter("x").num_instances(), len(dict(ampl.get_parameter("x")))
        )
        self.assertEqual(ampl.get_parameter("x").num_instances(), 1)
        self.assertEqual(ampl.get_parameter("y").num_instances(), 2)
        self.assertEqual(ampl.get_parameter("z").num_instances(), 4)
        self.assertEqual(ampl.get_parameter("xx").num_instances(), 4)
        self.assertEqual(ampl.get_parameter("yy").num_instances(), 8)
        self.assertEqual(ampl.get_parameter("zz").num_instances(), 8)
        self.assertEqual(max(p.num_instances() for name, p in ampl.get_parameters()), 8)
        self.assertEqual(
            ampl.get_parameter("x").name(), ampl.get_parameters()["x"].name()
        )
        with self.assertRaises(KeyError):
            ampl.get_parameter("notfound")
        with self.assertRaises(KeyError):
            ampl.get_parameters()["notfound"]

    def test_variable_iterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        self.assertEqual(len(ampl.get_variables()), ampl.get_variables().size())
        self.assertEqual(ampl.get_variables().size(), len(list(ampl.get_variables())))
        self.assertEqual(ampl.get_variables().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.get_variables().size(), 0)
        ampl.eval("var x;")
        self.assertEqual(ampl.get_variables().size(), 1)
        ampl.eval("var y{1..2};")
        self.assertEqual(ampl.get_variables().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        self.assertEqual(ampl.get_variables().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        self.assertEqual(ampl.get_variables().size(), 4)
        ampl.eval("var yy{1..2,4..5,7..8};")
        self.assertEqual(ampl.get_variables().size(), 5)
        ampl.eval('var zz{1..2,{"a", "b"}, 5..6};')
        self.assertEqual(ampl.get_variables().size(), 6)
        self.assertEqual(
            ampl.get_variable("x").num_instances(), len(dict(ampl.get_variable("x")))
        )
        self.assertEqual(ampl.get_variable("x").num_instances(), 1)
        self.assertEqual(ampl.get_variable("y").num_instances(), 2)
        self.assertEqual(ampl.get_variable("z").num_instances(), 4)
        self.assertEqual(ampl.get_variable("xx").num_instances(), 4)
        self.assertEqual(ampl.get_variable("yy").num_instances(), 8)
        self.assertEqual(ampl.get_variable("zz").num_instances(), 8)
        self.assertEqual(
            max(var.num_instances() for name, var in ampl.get_variables()), 8
        )
        self.assertEqual(
            ampl.get_variable("x").name(), ampl.get_variables()["x"].name()
        )
        with self.assertRaises(KeyError):
            ampl.get_variable("notfound")
        with self.assertRaises(KeyError):
            ampl.get_variables()["notfound"]

    def test_constraint_iterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.eval("s.t. c_x: x = 0;")
        self.assertEqual(ampl.get_constraints().size(), len(ampl.get_constraints()))
        self.assertEqual(
            ampl.get_constraints().size(), len(list(ampl.get_constraints()))
        )
        self.assertEqual(ampl.get_constraints().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.get_constraints().size(), 0)
        ampl.eval("var x;")
        ampl.eval("s.t. c_x: x = 0;")
        self.assertEqual(ampl.get_constraints().size(), 1)
        ampl.eval("var y{1..2};")
        ampl.eval("s.t. c_y{i in 1..2}: y[i] = i;")
        self.assertEqual(ampl.get_constraints().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        ampl.eval('s.t. c_z{(i, j) in {1..2, {"a", "b"}}}: z[i,j] = i;')
        self.assertEqual(ampl.get_constraints().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        ampl.eval("s.t. c_xx{(i, j) in {1..2,4..5}}: xx[i,j] = i+j;")
        self.assertEqual(ampl.get_constraints().size(), 4)
        self.assertEqual(
            ampl.get_constraint("c_x").num_instances(),
            len(dict(ampl.get_constraint("c_x"))),
        )
        self.assertEqual(ampl.get_constraint("c_x").num_instances(), 1)
        self.assertEqual(ampl.get_constraint("c_y").num_instances(), 2)
        self.assertEqual(ampl.get_constraint("c_z").num_instances(), 4)
        self.assertEqual(ampl.get_constraint("c_xx").num_instances(), 4)
        self.assertEqual(
            max(con.num_instances() for name, con in ampl.get_constraints()), 4
        )
        self.assertEqual(
            ampl.get_constraint("c_x").name(), ampl.get_constraints()["c_x"].name()
        )
        with self.assertRaises(KeyError):
            ampl.get_constraint("notfound")
        with self.assertRaises(KeyError):
            ampl.get_constraints()["notfound"]

    def test_objective_iterators(self):
        ampl = self.ampl
        ampl.eval("var x;")
        ampl.eval("maximize c_x: x;")
        self.assertEqual(ampl.get_objectives().size(), len(ampl.get_objectives()))
        self.assertEqual(ampl.get_objectives().size(), len(list(ampl.get_objectives())))
        self.assertEqual(ampl.get_objectives().size(), 1)
        ampl.eval("reset;")
        self.assertEqual(ampl.get_objectives().size(), 0)
        ampl.eval("var x;")
        ampl.eval("maximize c_x: x;")
        self.assertEqual(ampl.get_objectives().size(), 1)
        ampl.eval("var y{1..2};")
        ampl.eval("maximize c_y{i in 1..2}: y[i];")
        self.assertEqual(ampl.get_objectives().size(), 2)
        ampl.eval('var z{1..2, {"a", "b"}};')
        ampl.eval('maximize c_z{(i, j) in {1..2, {"a", "b"}}}: z[i,j];')
        self.assertEqual(ampl.get_objectives().size(), 3)
        ampl.eval("var xx{1..2,4..5};")
        ampl.eval("maximize c_xx{(i, j) in {1..2,4..5}}: xx[i,j];")
        self.assertEqual(ampl.get_objectives().size(), 4)
        self.assertEqual(
            ampl.get_objective("c_x").num_instances(),
            len(dict(ampl.get_objective("c_x"))),
        )
        self.assertEqual(ampl.get_objective("c_x").num_instances(), 1)
        self.assertEqual(ampl.get_objective("c_y").num_instances(), 2)
        self.assertEqual(ampl.get_objective("c_z").num_instances(), 4)
        self.assertEqual(ampl.get_objective("c_xx").num_instances(), 4)
        self.assertEqual(
            max(obj.num_instances() for name, obj in ampl.get_objectives()), 4
        )
        self.assertEqual(
            ampl.get_objective("c_x").name(), ampl.get_objectives()["c_x"].name()
        )
        with self.assertRaises(KeyError):
            ampl.get_objective("notfound")
        with self.assertRaises(KeyError):
            ampl.get_objectives()["notfound"]


if __name__ == "__main__":
    unittest.main()
