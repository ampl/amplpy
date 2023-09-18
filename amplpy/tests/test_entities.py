#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import amplpy
from . import TestBase

try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None


def load_diet_model(ampl):
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

    def test_variable(self):
        load_diet_model(self.ampl)
        ampl = self.ampl
        # ampl.solve()
        self.assertEqual(
            ampl.get_variable("Buy").num_instances(), ampl.get_set("FOOD").size()
        )
        f_min = ampl.get_parameter("f_min")
        f_max = ampl.get_parameter("f_max")
        buy = ampl.get_variable("Buy")
        buy["BEEF"] = 10
        self.assertEqual(buy["BEEF"].value(), 10)
        self.assertTrue(isinstance(buy.get_values(), amplpy.DataFrame))
        self.assertTrue(isinstance(buy.get_values(["val"]), amplpy.DataFrame))
        self.assertTrue(isinstance(buy.get_values("val"), amplpy.DataFrame))
        for index, var in ampl.get_variable("Buy"):
            self.assertTrue(isinstance(var.value(), float))
            var.set_value(f_min[index])
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
            self.assertTrue(isinstance(var.sstatus(), str))
            self.assertTrue(isinstance(var.status(), str))

    def test_variable_numpy(self):
        if np is None:
            self.skipTest("numpy not available")
        ampl = self.ampl
        ampl.eval("var v_indexed{1..3};")
        ampl.var["v_indexed"][2] = np.int64(123)
        self.assertEqual(ampl.var["v_indexed"][2].value(), 123)
        ampl.eval("var v_scalar;")
        ampl.var["v_scalar"] = np.int64(456)
        self.assertEqual(ampl.var["v_scalar"].value(), 456)

    def test_constraint(self):
        load_diet_model(self.ampl)
        ampl = self.ampl
        # ampl.solve()
        self.assertEqual(
            ampl.get_constraint("diet").num_instances(), ampl.get_set("NUTR").size()
        )
        for _, con in ampl.get_constraint("diet"):
            self.assertTrue(isinstance(con.is_logical(), bool))
            con.drop()
            con.restore()
            self.assertTrue(isinstance(con.body(), float))
            self.assertTrue(isinstance(con.astatus(), str))
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
            self.assertTrue(isinstance(con.status(), str))
            self.assertTrue(isinstance(con.sstatus(), str))
            con.setDual(0)
            self.assertEqual(con.val(), None)
        ampl.eval(
            """
            var x;
            var y;
            s.t. xy: x <==> y;
        """
        )
        self.assertTrue(ampl.get_constraint("xy").is_logical())
        self.assertTrue(isinstance(ampl.get_constraint("xy").val(), float))

    def test_set(self):
        load_diet_model(self.ampl)
        ampl = self.ampl
        self.assertEqual(ampl.get_set("FOOD").to_string(), "set FOOD;")
        self.assertEqual(str(ampl.get_set("FOOD")), "set FOOD;")
        self.assertEqual(
            ampl.get_set("NUTR").size(),
            len(ampl.get_set("NUTR").members()),
        )
        self.assertEqual(
            len(ampl.get_set("NUTR").members()),
            len(list(ampl.get_set("NUTR").members())),
        )
        self.assertTrue(ampl.get_set("NUTR").contains("A"))
        self.assertTrue(ampl.get_set("NUTR").contains(("B1",)))
        self.assertFalse(ampl.get_set("NUTR").contains("X"))
        for _, st in ampl.get_sets():
            self.assertTrue(isinstance(st.arity(), int))
            self.assertEqual(st.arity(), 1)
            self.assertTrue(isinstance(st.size(), int))
            self.assertEqual(len(st.instances()), 1)
            self.assertEqual(len(dict(st.instances())), len(list(st.instances())))
            self.assertTrue(isinstance(st.arity(), int))
        ampl.eval("model; set T{1..2}; set T2{1..2};")
        ampl.get_set("T")[1] = [-1, -2]
        self.assertEqual(ampl.get_set("T").get((1,)).get_values().to_list(), [-1, -2])
        self.assertEqual(ampl.get_set("T").find((3,)), None)
        self.assertIsInstance(ampl.get_set("T").find(1), amplpy.Set)
        ampl.get_set("T")[1].set_values([1, 2])
        self.assertEqual(ampl.get_set("T")[1].get_values().to_list(), [1, 2])
        ampl.get_set("T")[2].set_values(["1", 2])
        self.assertEqual(ampl.get_set("T")[2].get_values().to_list(), ["1", 2])
        ampl.get_set("T2")[1].set_values(ampl.get_set("T")[1].get_values())
        self.assertEqual(ampl.get_set("T2")[1].get_values().to_list(), [1, 2])
        ampl.get_set("T2")[2].set_values(ampl.get_set("T")[2].get_values())
        self.assertEqual(ampl.get_set("T2")[2].get_values().to_list(), ["1", 2])
        ampl.eval("set T3 dimen 2; set T4 dimen 2;")
        ampl.get_set("T3").set_values([(1, 2)])
        self.assertEqual(ampl.get_set("T3").get_values().to_list(), [(1, 2)])
        ampl.get_set("T3").set_values(set([("b", 1), ("a", 2)]))
        self.assertEqual(
            sorted(ampl.get_set("T3").get_values().to_list()), [("a", 2), ("b", 1)]
        )
        ampl.eval("set T5;")
        ampl.set["T5"] = set(["a", "b", "c"])
        self.assertEqual(
            sorted(ampl.get_set("T5").get_values().to_list()), ["a", "b", "c"]
        )

    def test_parameter(self):
        load_diet_model(self.ampl)
        ampl = self.ampl
        self.assertEqual(
            ampl.get_set("FOOD").size(), ampl.get_parameter("cost").num_instances()
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
        self.assertFalse(ampl.get_parameter("a").has_default())
        self.assertTrue(ampl.get_parameter("b").has_default())
        self.assertFalse(ampl.get_parameter("a").is_symbolic())
        self.assertFalse(ampl.get_parameter("b").is_symbolic())
        self.assertTrue(ampl.get_parameter("c").is_symbolic())
        cost = ampl.get_parameter("cost")
        self.assertEqual(cost.indexarity(), 1)
        self.assertEqual(cost.get_indexing_sets(), ["FOOD"])
        self.assertEqual(cost.xref(), ["total_cost"])
        for i, food in enumerate(ampl.get_set("FOOD").members()):
            cost[food] = i + 1
            self.assertEqual(cost[food], i + 1)
            cost.set(food, i + 2)
            self.assertEqual(cost[food], i + 2)
        a = ampl.get_parameter("a")
        a.set(10)
        self.assertEqual(a.value(), 10)
        c = ampl.get_parameter("c")
        b = ampl.get_parameter("c")
        c.set("a")
        self.assertEqual(c.value(), "a")
        self.assertEqual(b.value(), "a")
        self.assertEqual(b.indexarity(), 0)
        self.assertEqual(a.is_scalar(), True)
        self.assertEqual(b.is_scalar(), True)
        self.assertEqual(c.is_scalar(), True)
        d = ampl.get_parameter("d")
        self.assertEqual(d.is_scalar(), False)
        d.set(1, "a")
        self.assertEqual(d[1], "a")
        d[1] = "aa"
        self.assertEqual(d[1], "aa")
        d.set(2, "b")
        self.assertEqual(d[2], "b")
        d.set_values({1: "x", 2: "y"})
        self.assertEqual(d[1], "x")
        self.assertEqual(d[2], "y")
        d.set_values(["xx", "yy"])
        self.assertEqual(d[1], "xx")
        self.assertEqual(d[2], "yy")
        d2 = ampl.get_parameter("d2")
        d2.set_values(d.get_values())
        self.assertEqual(d2[1], "xx")
        self.assertEqual(d2[2], "yy")
        self.assertEqual(cost.is_scalar(), False)
        ampl.eval("param cost2{FOOD};")
        self.assertTrue(isinstance(cost.get_values(), amplpy.DataFrame))
        cost2 = ampl.get_parameter("cost2")
        cost2.set_values(cost.get_values())
        for food in ampl.get_set("FOOD").members():
            self.assertEqual(cost2[food], cost[food])

    def test_parameter_numpy(self):
        if np is None:
            self.skipTest("numpy not available")
        ampl = self.ampl
        ampl.eval("param p_indexed{1..3};")
        ampl.get_parameter("p_indexed").set_values(np.array([4, 5, 6]))
        self.assertEqual(
            ampl.get_parameter("p_indexed").get_values().to_list(),
            [(1, 4), (2, 5), (3, 6)],
        )
        ampl.eval("param p_scalar;")
        ampl.get_parameter("p_scalar").set(np.int64(123))
        self.assertEqual(ampl.get_parameter("p_scalar").value(), 123)
        ampl.get_parameter("p_indexed").set(2, np.int64(456))
        self.assertEqual(ampl.get_parameter("p_indexed").get(2), 456)

    def test_parameter_numpy_array(self):
        if np is None:
            self.skipTest("numpy not available")
        ampl = self.ampl
        ampl.eval(
            r"""
        set I;
        set J;
        param p{I, J};
        """
        )
        values = np.array([1, 2, 3])
        n, k = values.shape[0], 1
        ampl.set["I"] = range(n)
        ampl.set["J"] = range(k)
        ampl.param["p"] = values
        self.assertEqual(ampl.param["p"].to_dict(), {(0, 0): 1, (1, 0): 2, (2, 0): 3})

    def test_parameter_numpy_ndarray(self):
        if np is None:
            self.skipTest("numpy not available")
        ampl = self.ampl
        ampl.eval(
            r"""
        set I;
        set J;
        param p{I, J};
        """
        )
        values = np.array(
            [
                [1, 2, 3],
                [4, 5, 6],
            ]
        )
        n, k = values.shape
        ampl.set["I"] = range(n)
        ampl.set["J"] = range(k)
        ampl.param["p"] = values
        self.assertEqual(
            ampl.param["p"].to_dict(),
            {
                (0, 0): 1,
                (0, 1): 2,
                (0, 2): 3,
                (1, 0): 4,
                (1, 1): 5,
                (1, 2): 6,
            },
        )

    def test_set_numpy(self):
        if np is None:
            self.skipTest("numpy not available")
        ampl = self.ampl
        ampl.eval("set A dimen 1;")
        ampl.get_set("A").set_values(np.array([4, 5, 6]))
        self.assertEqual(
            ampl.get_set("A").get_values().to_list(),
            [4, 5, 6],
        )
        ampl.eval("set B dimen 2;")
        ampl.get_set("B").set_values(np.array([[4, 1], [5, 2], [6, 3]]))
        self.assertEqual(
            ampl.get_set("B").get_values().to_list(),
            [(4, 1), (5, 2), (6, 3)],
        )

    def test_set_iterable(self):
        ampl = self.ampl
        ampl.eval("set A dimen 1;")
        ampl.get_set("A").set_values([1, 2, "A", "1", "2"])
        self.assertEqual(
            ampl.get_set("A").get_values().to_list(),
            [1, 2, "A", "1", "2"],
        )
        self.assertEqual(ampl.get_set("A").size(), 5)
        self.assertEqual(ampl.get_set("A").arity(), 1)
        ampl.eval("set B dimen 2;")
        ampl.get_set("B").set_values([[4, 1], [5, 2], [6, 3]])
        self.assertEqual(
            ampl.get_set("B").get_values().to_list(),
            [(4, 1), (5, 2), (6, 3)],
        )
        self.assertEqual(ampl.get_set("B").size(), 3)
        self.assertEqual(ampl.get_set("B").arity(), 2)
        with self.assertRaises(ValueError):
            ampl.get_set("A").set_values([1, (2, 1), "A", "1", "2"])
        with self.assertRaises(ValueError):
            ampl.get_set("A").set_values([(2, 1), (3, 4)])
        with self.assertRaises(ValueError):
            ampl.get_set("B").set_values([1, "A", "1", "2"])
        with self.assertRaises(ValueError):
            ampl.get_set("B").set_values([1, 2])

    def test_precision(self):
        pi = 3.1415926535897932384626433832795028841971
        ampl = self.ampl
        ampl.eval("param x;")
        ampl.get_parameter("x").set(pi)
        ampl.eval("display x;")  # invalidate cache
        self.assertEqual(ampl.param["x"].value(), pi)

    def test_infinity(self):
        inf = float("inf")
        ampl = self.ampl
        ampl.eval("param x;")
        ampl.get_parameter("x").set(inf)
        self.assertEqual(ampl.get_value("x"), inf)
        self.assertTrue(isinstance(ampl.get_value("x"), float))
        ampl.get_parameter("x").set(5)
        self.assertEqual(ampl.get_value("x"), 5)
        self.assertTrue(isinstance(ampl.get_value("x"), int))
        ampl.eval("param y{1..3};")
        ampl.get_parameter("y").set_values([inf] * 3)
        for i in range(3):
            self.assertEqual(ampl.get_value(f"y[{i+1}]"), inf)

    def test_objective(self):
        load_diet_model(self.ampl)
        ampl = self.ampl
        obj = ampl.get_objective("total_cost")
        self.assertEqual(ampl.get_current_objective().name(), "total_cost")
        self.assertEqual(len(dict(obj)), obj.num_instances())
        self.assertTrue(isinstance(obj.value(), float))
        self.assertTrue(isinstance(obj.astatus(), str))
        self.assertTrue(isinstance(obj.sstatus(), str))
        self.assertTrue(isinstance(obj.exitcode(), int))
        self.assertTrue(isinstance(obj.message(), str))
        self.assertTrue(isinstance(obj.result(), str))
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
        self.assertEqual(ampl.get_current_objective(), None)
        ampl.eval("objective A;")
        self.assertEqual(ampl.get_current_objective().name(), "A")
        self.assertFalse(ampl.get_current_objective().minimization())
        ampl.eval("objective B;")
        self.assertEqual(ampl.get_current_objective().name(), "B")
        self.assertTrue(ampl.get_current_objective().minimization())
        ampl.eval("objective C;")
        self.assertEqual(ampl.get_current_objective().name(), "C")
        self.assertFalse(ampl.get_current_objective().minimization())
        ampl.eval("objective A;")
        self.assertEqual(ampl.get_current_objective().name(), "A")
        self.assertFalse(ampl.get_current_objective().minimization())

    def test_set_values(self):
        ampl = self.ampl
        ampl.eval("var x{1..3};")
        d = {1: 2, 2: 5, 3: 9}
        ampl.var["x"].set_values(d)
        self.assertEqual(d, ampl.var["x"].get_values().to_dict())

        d = {1: 11, 2: 55, 3: 99}
        ampl.var["x"] = d
        self.assertEqual(d, ampl.var["x"].get_values().to_dict())

    def test_valid_data(self):
        ampl = self.ampl
        ampl.eval("set I ordered; param P{I};")
        ampl.eval("data; set I := 1 2; param P := 2 1 1 3;")
        self.assertEqual(
            ampl.get_parameter("P").get_values().to_list(), [(1, 3), (2, 1)]
        )
        self.assertEqual(ampl.get_data("P").to_list(), [(1, 3), (2, 1)])

    def test_invalid_data(self):
        ampl = self.ampl
        ampl.eval("set I ordered; param P{I};")
        ampl.eval("data; set I := 1 2; param P := 2 1 1 3 3 0;")
        with self.assertRaises(RuntimeError):
            print(ampl.get_parameter("P").get_values())
        ampl.eval("reset data; data; set I := 1 2; param P := 2 1 1 3 3 0;")
        with self.assertRaises(RuntimeError):
            print(ampl.get_data("P"))

    def test_entity_get_values_aliases(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval("param p{i in 1..10, j in 1..10} := i*j;")
        self.assertTrue(
            ampl.get_parameter("p")
            .to_pandas()
            .equals(ampl.get_parameter("p").get_values().to_pandas())
        )
        self.assertTrue(
            ampl.get_parameter("p")
            .to_pandas(multi_index=False)
            .equals(ampl.get_parameter("p").get_values().to_pandas(multi_index=False))
        )
        self.assertEqual(
            ampl.get_parameter("p").to_list(),
            ampl.get_parameter("p").get_values().to_list(),
        )
        self.assertEqual(
            ampl.get_parameter("p").to_list(skip_index=True),
            ampl.get_parameter("p").get_values().to_list(skip_index=True),
        )
        self.assertEqual(
            ampl.get_parameter("p").to_list(skip_index=True),
            [i * j for i in range(1, 10 + 1) for j in range(1, 10 + 1)],
        )
        self.assertEqual(
            ampl.get_parameter("p").to_dict(),
            ampl.get_parameter("p").get_values().to_dict(),
        )

    def test_stack(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval(
            """
        set PRODUCTS;
        set RESOURCES;
        param need {RESOURCES,PRODUCTS} >= 0;
        """
        )
        need_dict = {
            "U": {"M": 10.0, "A": 1.0, "B": 2.0},
            "V": {"M": 9.0, "A": 1.0, "B": 1.0},
        }
        PRODUCTS = ["U", "V"]
        RESOURCES = ["M", "A", "B"]
        ampl.set["PRODUCTS"] = PRODUCTS
        ampl.set["RESOURCES"] = RESOURCES
        ampl.param["need"] = pd.DataFrame(
            [
                [10, 1, 2],
                [9, 1, 1],
            ],
            columns=RESOURCES,
            index=PRODUCTS,
        ).transpose()
        self.assertEqual(
            ampl.param["need"].to_dict(),
            {
                (r, p): value
                for p, rdict in need_dict.items()
                for r, value in rdict.items()
            },
        )


if __name__ == "__main__":
    unittest.main()
