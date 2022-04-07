#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted
from past.builtins import basestring

from . import TestBase
import unittest
import amplpy


def loadDietModel(ampl):
    ampl.eval(
        """
        set FOOD ;
        set NUTR ;
        # Parameters
        param cost { FOOD } > 0;
        param f_min { FOOD } >= 0;
        param f_max {j in FOOD } >= f_min [j];
        param n_min { NUTR } >= 0;
        param n_max {i in NUTR } >= n_min [i];
        param amt {NUTR , FOOD } >= 0;
        # Variables
        var Buy {j in FOOD } >= f_min [j], <= f_max [j];
        # Objective
        minimize total_cost : sum {j in FOOD } cost [j] * Buy[j];
        # Contraints
        subject to diet {i in NUTR }:
            n_min [i] <= sum {j in FOOD } amt[i,j] * Buy[j] <= n_max [i];
    """
    )
    ampl.eval(
        """
        data;
        set NUTR := A C B1 B2 NA CAL;
        set FOOD := BEEF CHK FISH HAM MCH MTL SPG TUR ;
        param : cost f_min f_max :=
        BEEF 3.19 2 10
        CHK 2.59 2 10
        FISH 2.29 2 10
        HAM 2.89 2 10
        MCH 1.89 2 10
        MTL 1.99 2 10
        SPG 1.99 2 10
        TUR 2.49 2 10 ;
        param : n_min n_max :=
        A 700 20000
        C 700 20000
        B1 700 20000
        B2 700 20000
        NA 0 50000
        CAL 16000 24000 ;
        param amt (tr):
        A C B1 B2 NA CAL :=
        BEEF 60 20 10 15 938 295
        CHK 8 0 20 20 2180 770
        FISH 8 10 15 10 945 440
        HAM 40 40 35 10 278 430
        MCH 15 35 15 15 1182 315
        MTL 70 30 15 15 896 400
        SPG 25 50 25 15 1329 370
        TUR 60 20 15 10 1397 450 ;
    """
    )


class TestEntities(TestBase.TestBase):
    """Test entities."""

    def testVariable(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        # ampl.solve()
        self.assertEqual(
            ampl.getVariable("Buy").numInstances(), ampl.getSet("FOOD").size()
        )
        f_min = ampl.getParameter("f_min")
        f_max = ampl.getParameter("f_max")
        Buy = ampl.getVariable("Buy")
        Buy["BEEF"] = 10
        self.assertEqual(Buy["BEEF"].value(), 10)
        self.assertTrue(isinstance(Buy.getValues(), amplpy.DataFrame))
        self.assertTrue(isinstance(Buy.getValues(["val"]), amplpy.DataFrame))
        for index, var in ampl.getVariable("Buy"):
            self.assertTrue(isinstance(var.value(), float))
            var.setValue(f_min[index])
            self.assertEqual(var.value(), f_min[index])
            var.fix()
            self.assertEqual(var.astatus(), "fix")
            var.unfix()
            self.assertEqual(var.astatus(), "in")
            var.fix(f_max[index])
            self.assertEqual(var.value(), f_max[index])
            self.assertTrue(isinstance(var.defeqn(), int))
            self.assertTrue(isinstance(var.dual(), float))
            self.assertTrue(isinstance(var.init(), float))
            self.assertTrue(isinstance(var.init0(), float))
            self.assertTrue(isinstance(var.lb(), float))
            self.assertGreaterEqual(var.lb(), f_min[index])
            self.assertTrue(isinstance(var.ub(), float))
            self.assertLessEqual(var.ub(), f_max[index])
            self.assertTrue(isinstance(var.lb0(), float))
            self.assertEqual(var.lb0(), f_min[index])
            self.assertTrue(isinstance(var.ub0(), float))
            self.assertEqual(var.ub0(), f_max[index])
            self.assertTrue(isinstance(var.lb1(), float))
            self.assertGreaterEqual(var.lb1(), f_min[index])
            self.assertTrue(isinstance(var.ub1(), float))
            self.assertLessEqual(var.ub1(), f_max[index])
            self.assertTrue(isinstance(var.lb2(), float))
            self.assertGreaterEqual(var.lb2(), f_min[index])
            self.assertTrue(isinstance(var.ub2(), float))
            self.assertLessEqual(var.ub2(), f_max[index])
            self.assertTrue(isinstance(var.lrc(), float))
            self.assertTrue(isinstance(var.urc(), float))
            self.assertTrue(isinstance(var.lslack(), float))
            self.assertTrue(isinstance(var.uslack(), float))
            self.assertTrue(isinstance(var.rc(), float))
            self.assertTrue(isinstance(var.slack(), float))
            self.assertTrue(isinstance(var.sstatus(), basestring))
            self.assertTrue(isinstance(var.status(), basestring))

    def testConstraint(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        # ampl.solve()
        self.assertEqual(
            ampl.getConstraint("diet").numInstances(), ampl.getSet("NUTR").size()
        )
        for index, con in ampl.getConstraint("diet"):
            self.assertTrue(isinstance(con.isLogical(), bool))
            con.drop()
            con.restore()
            self.assertTrue(isinstance(con.body(), float))
            self.assertTrue(isinstance(con.astatus(), basestring))
            self.assertEqual(con.astatus(), "in")
            con.drop()
            self.assertEqual(con.astatus(), "drop")
            con.restore()
            self.assertEqual(con.astatus(), "in")
            self.assertTrue(isinstance(con.defvar(), int))
            self.assertTrue(isinstance(con.dinit(), float))
            self.assertTrue(isinstance(con.dinit0(), float))
            self.assertTrue(isinstance(con.dual(), float))
            self.assertTrue(isinstance(con.lb(), float))
            self.assertTrue(isinstance(con.ub(), float))
            self.assertTrue(isinstance(con.lbs(), float))
            self.assertTrue(isinstance(con.ubs(), float))
            self.assertTrue(isinstance(con.ldual(), float))
            self.assertTrue(isinstance(con.udual(), float))
            self.assertTrue(isinstance(con.lslack(), float))
            self.assertTrue(isinstance(con.uslack(), float))
            self.assertTrue(isinstance(con.slack(), float))
            self.assertTrue(isinstance(con.status(), basestring))
            self.assertTrue(isinstance(con.sstatus(), basestring))
            con.setDual(0)
            self.assertEqual(con.val(), None)
        ampl.eval(
            """
            var x;
            var y;
            s.t. xy: x <==> y;
        """
        )
        self.assertTrue(ampl.getConstraint("xy").isLogical())
        self.assertTrue(isinstance(ampl.getConstraint("xy").val(), float))

    def testSet(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        self.assertEqual(ampl.getSet("FOOD").toString(), "set FOOD;")
        self.assertEqual(str(ampl.getSet("FOOD")), "set FOOD;")
        self.assertEqual(
            ampl.getSet("NUTR").size(),
            len(ampl.getSet("NUTR").members()),
        )
        self.assertEqual(
            len(ampl.getSet("NUTR").members()), len(list(ampl.getSet("NUTR").members()))
        )
        self.assertTrue(ampl.getSet("NUTR").contains("A"))
        self.assertTrue(ampl.getSet("NUTR").contains(("B1",)))
        self.assertFalse(ampl.getSet("NUTR").contains("X"))
        for name, st in ampl.getSets():
            self.assertTrue(isinstance(st.arity(), int))
            self.assertEqual(st.arity(), 1)
            self.assertTrue(isinstance(st.size(), int))
            self.assertEqual(len(st.instances()), 1)
            self.assertEqual(len(dict(st.instances())), len(list(st.instances())))
            self.assertTrue(isinstance(st.arity(), int))
        ampl.eval("model; set T{1..2}; set T2{1..2};")
        ampl.getSet("T")[1] = [-1, -2]
        self.assertEqual(ampl.getSet("T").get((1,)).getValues().toList(), [-1, -2])
        self.assertEqual(ampl.getSet("T").find((3,)), None)
        self.assertIsInstance(ampl.getSet("T").find(1), amplpy.Set)
        ampl.getSet("T")[1].setValues([1, 2])
        self.assertEqual(ampl.getSet("T")[1].getValues().toList(), [1, 2])
        ampl.getSet("T")[2].setValues(["1", 2])
        self.assertEqual(ampl.getSet("T")[2].getValues().toList(), ["1", 2])
        ampl.getSet("T2")[1].setValues(ampl.getSet("T")[1].getValues())
        self.assertEqual(ampl.getSet("T2")[1].getValues().toList(), [1, 2])
        ampl.getSet("T2")[2].setValues(ampl.getSet("T")[2].getValues())
        self.assertEqual(ampl.getSet("T2")[2].getValues().toList(), ["1", 2])
        ampl.eval("set T3 dimen 2; set T4 dimen 2;")
        ampl.getSet("T3").setValues([(1, 2)])
        self.assertEqual(ampl.getSet("T3").getValues().toList(), [(1, 2)])
        ampl.getSet("T3").setValues(set([("b", 1), ("a", 2)]))
        self.assertEqual(
            sorted(ampl.getSet("T3").getValues().toList()), [("a", 2), ("b", 1)]
        )
        ampl.eval("set T5;")
        ampl.set["T5"] = set(["a", "b", "c"])
        self.assertEqual(
            sorted(ampl.getSet("T5").getValues().toList()), ["a", "b", "c"]
        )

        try:
            import numpy as np
        except ImportError:
            pass
        else:
            ampl.getSet("T")[1].setValues(np.array([1, 2]))
            self.assertEqual(ampl.getSet("T")[1].size(), 2)
            ampl.getSet("T3").setValues(np.array([[1, 2], [3, 4]]))
            self.assertEqual(ampl.getSet("T3").size(), 2)

    def testParameter(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        self.assertEqual(
            ampl.getSet("FOOD").size(), ampl.getParameter("cost").numInstances()
        )
        ampl.eval(
            """
            param a;
            param b default a;
            param c symbolic;
            param d{1..2} symbolic;
            param d2{1..2} symbolic;
        """
        )
        self.assertFalse(ampl.getParameter("a").hasDefault())
        self.assertTrue(ampl.getParameter("b").hasDefault())
        self.assertFalse(ampl.getParameter("a").isSymbolic())
        self.assertFalse(ampl.getParameter("b").isSymbolic())
        self.assertTrue(ampl.getParameter("c").isSymbolic())
        cost = ampl.getParameter("cost")
        self.assertEqual(cost.indexarity(), 1)
        self.assertEqual(cost.getIndexingSets(), ["FOOD"])
        self.assertEqual(cost.xref(), ["total_cost"])
        for i, food in enumerate(ampl.getSet("FOOD").members()):
            cost[food] = i + 1
            self.assertEqual(cost[food], i + 1)
            cost.set(food, i + 2)
            self.assertEqual(cost[food], i + 2)
        a = ampl.getParameter("a")
        a.set(10)
        self.assertEqual(a.value(), 10)
        c = ampl.getParameter("c")
        b = ampl.getParameter("c")
        c.set("a")
        self.assertEqual(c.value(), "a")
        self.assertEqual(b.value(), "a")
        self.assertEqual(b.indexarity(), 0)
        self.assertEqual(a.isScalar(), True)
        self.assertEqual(b.isScalar(), True)
        self.assertEqual(c.isScalar(), True)
        d = ampl.getParameter("d")
        self.assertEqual(d.isScalar(), False)
        d.set(1, "a")
        self.assertEqual(d[1], "a")
        d[1] = "aa"
        self.assertEqual(d[1], "aa")
        d.set(2, "b")
        self.assertEqual(d[2], "b")
        d.setValues({1: "x", 2: "y"})
        self.assertEqual(d[1], "x")
        self.assertEqual(d[2], "y")
        d.setValues(["xx", "yy"])
        self.assertEqual(d[1], "xx")
        self.assertEqual(d[2], "yy")
        d2 = ampl.getParameter("d2")
        d2.setValues(d.getValues())
        self.assertEqual(d2[1], "xx")
        self.assertEqual(d2[2], "yy")
        self.assertEqual(cost.isScalar(), False)
        ampl.eval("param cost2{FOOD};")
        self.assertTrue(isinstance(cost.getValues(), amplpy.DataFrame))
        cost2 = ampl.getParameter("cost2")
        cost2.setValues(cost.getValues())
        for food in ampl.getSet("FOOD").members():
            self.assertEqual(cost2[food], cost[food])

        try:
            import numpy as np
        except ImportError:
            pass
        else:
            ampl.eval("param lst{1..3};")
            ampl.getParameter("lst").setValues(np.array([1, 2, 3]))

    def testPrecision(self):
        PI = 3.1415926535897932384626433832795028841971
        ampl = self.ampl
        ampl.eval("param x;")
        ampl.getParameter("x").set(PI)
        ampl.eval("display x;")  # invalidate cache
        self.assertEqual(ampl.param["x"].value(), PI)

    def testInfinity(self):
        inf = float("inf")
        ampl = self.ampl
        ampl.eval("param x;")
        ampl.getParameter("x").set(inf)
        self.assertEqual(ampl.getValue("x"), inf)
        ampl.eval("param y{1..3};")
        ampl.getParameter("y").setValues([inf] * 3)
        for i in range(3):
            self.assertEqual(ampl.getValue("y[{}]".format(i + 1)), inf)

    def testObjective(self):
        loadDietModel(self.ampl)
        ampl = self.ampl
        obj = ampl.getObjective("total_cost")
        self.assertEqual(ampl.getCurrentObjective().name(), "total_cost")
        self.assertEqual(len(dict(obj)), obj.numInstances())
        self.assertTrue(isinstance(obj.value(), float))
        self.assertTrue(isinstance(obj.astatus(), basestring))
        self.assertTrue(isinstance(obj.sstatus(), basestring))
        self.assertTrue(isinstance(obj.exitcode(), int))
        self.assertTrue(isinstance(obj.message(), basestring))
        self.assertTrue(isinstance(obj.result(), basestring))
        obj.drop()
        self.assertEqual(obj.astatus(), "drop")
        obj.restore()
        self.assertEqual(obj.astatus(), "in")
        self.assertTrue(obj.minimization())
        ampl.eval(
            """
            maximize A: 1;
            minimize B: 1;
            maximize C: 1;
        """
        )
        self.assertEqual(ampl.getCurrentObjective(), None)
        ampl.eval("objective A;")
        self.assertEqual(ampl.getCurrentObjective().name(), "A")
        self.assertFalse(ampl.getCurrentObjective().minimization())
        ampl.eval("objective B;")
        self.assertEqual(ampl.getCurrentObjective().name(), "B")
        self.assertTrue(ampl.getCurrentObjective().minimization())
        ampl.eval("objective C;")
        self.assertEqual(ampl.getCurrentObjective().name(), "C")
        self.assertFalse(ampl.getCurrentObjective().minimization())
        ampl.eval("objective A;")
        self.assertEqual(ampl.getCurrentObjective().name(), "A")
        self.assertFalse(ampl.getCurrentObjective().minimization())

    def testSetValues(self):
        ampl = self.ampl
        ampl.eval("var x{1..3};")
        d = {1: 2, 2: 5, 3: 9}
        ampl.var["x"].setValues(d)
        self.assertEqual(d, ampl.var["x"].getValues().toDict())

        d = {1: 11, 2: 55, 3: 99}
        ampl.var["x"] = d
        self.assertEqual(d, ampl.var["x"].getValues().toDict())


if __name__ == "__main__":
    unittest.main()
