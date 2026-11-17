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

    def test_drop_restore_instances(self):
        ampl = self.ampl
        for declaration, collection, operator in (
            ("s.t. c", ampl.con, ">="),
            ("minimize c", ampl.obj, "+"),
        ):
            for indexing, expression, target in (
                ("{t in 1..3}", f"x {operator} t", 2),
                ("{s in {'a', 'b', 'c'}}", f"x {operator} 1", "b"),
                ("{s in {'a', 'b'}, t in 1..2}", f"x {operator} t", ("b", 2)),
            ):
                with self.subTest(declaration=declaration, indexing=indexing):
                    ampl.reset()
                    # Keep active constraints from being eliminated by presolve.
                    ampl.option["presolve"] = 0
                    ampl.eval(f"var x; {declaration}{indexing}: {expression};")
                    entity = collection["c"]
                    indices = [index for index, _ in entity]
                    target_index = target if isinstance(target, tuple) else (target,)
                    entity[target].drop()
                    self.assertEqual(
                        [entity[index].astatus() for index in indices],
                        ["drop" if index == target_index else "in" for index in indices],
                    )
                    entity[target].restore()
                    self.assertEqual(
                        [entity[index].astatus() for index in indices],
                        ["in"] * len(indices),
                    )
                    entity.drop()
                    self.assertEqual(
                        [entity[index].astatus() for index in indices],
                        ["drop"] * len(indices),
                    )
                    # Iterated instances must retain their indices too.
                    for index, instance in entity:
                        if index == target_index:
                            instance.restore()
                    self.assertEqual(
                        [entity[index].astatus() for index in indices],
                        ["in" if index == target_index else "drop" for index in indices],
                    )
                    entity.restore()
                    self.assertEqual(
                        [entity[index].astatus() for index in indices],
                        ["in"] * len(indices),
                    )

            with self.subTest(declaration=declaration, indexing="scalar"):
                ampl.reset()
                ampl.option["presolve"] = 0
                ampl.eval(f"var x; {declaration}: x {operator} 1;")
                entity = collection["c"]
                entity.drop()
                self.assertEqual(entity.astatus(), "drop")
                entity.restore()
                self.assertEqual(entity.astatus(), "in")

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

    def test_indexed_set(self):
        ampl = self.ampl
        ampl.eval(
            r"""
        set I;
        set J{I};
        """
        )
        self.assertEqual(ampl.set["I"].is_scalar(), True)
        self.assertEqual(ampl.set["J"].is_scalar(), False)
        ampl.set["I"] = range(10)
        ampl.set["J"] = {i: range(i) for i in range(10)}
        self.assertEqual(ampl.set["I"].size(), 10)
        self.assertEqual(list(ampl.set["I"].members()), list(range(10)))
        for i in range(10):
            self.assertEqual(ampl.set["J"][i].size(), i)
            self.assertEqual(list(ampl.set["J"][i].members()), list(range(i)))

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
        self.assertEqual(obj, obj.get())
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

    def test_objective_indexed(self):
        ampl = self.ampl
        ampl.eval(
            """
            set I;
            minimize obj{i in I}: i;
        """
        )
        ampl.set["I"] = range(10)
        obj = ampl.get_objective("obj")
        for i in range(10):
            self.assertEqual(obj[i].value(), i)
            self.assertEqual(obj[i].minimization(), True)
            self.assertEqual(obj[i].result(), "'?'")
            self.assertEqual(obj[i].message(), "'?'")
            self.assertEqual(obj[i].astatus(), "in")
            self.assertEqual(obj[i].sstatus(), "none")
        ampl.solve()
        for i in range(10):
            self.assertEqual(obj[i].value(), i)
            self.assertEqual(obj[i].minimization(), True)
            self.assertEqual(obj[i].result(), "solved")
            self.assertEqual(obj[i].message(), "'No variables declared.'")
            self.assertEqual(obj[i].astatus(), "in")
            self.assertEqual(obj[i].sstatus(), "none")

    def test_set_suffix(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval(
            """
            set I := 1..3;
            var x {I} >= 0;
            s.t. c {i in I}: x[i] <= i;
            var y;
            suffix rhspen IN;
        """
        )
        c = ampl.get_constraint("c")
        c.set_suffix("rhspen", pd.Series([10.0, 20.0, 30.0], index=[1, 2, 3]))
        self.assertEqual(
            [ampl.get_value(f"c[{i}].rhspen") for i in range(1, 4)], [10, 20, 30]
        )
        c.set_suffix("rhspen", pd.DataFrame({"rhspen": [5.0]}, index=[2]))
        self.assertEqual(ampl.get_value("c[2].rhspen"), 5)
        c[3].set_suffix("rhspen", 7)
        self.assertEqual(ampl.get_value("c[3].rhspen"), 7)
        ampl.get_variable("y").set_suffix("rhspen", 4)
        self.assertEqual(ampl.get_value("y.rhspen"), 4)

    def test_empty_data_assignment(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval(
            """
            set E default {};
            var x >= 0;
            var z {E};
            param p {E};
            subject to c {i in E}: x <= 1;
            suffix rhspen IN;
        """
        )
        c = ampl.get_constraint("c")
        z = ampl.get_variable("z")
        p = ampl.get_parameter("p")
        self.assertEqual(c.num_instances(), 0)
        # Empty data must be a no-op and must not terminate the process or
        # the AMPL interpreter.
        c.set_suffix("rhspen", pd.Series(-1.0, index=pd.Index([])))
        c.set_suffix("rhspen", pd.DataFrame({"rhspen": []}))
        c.set_suffix("rhspen", amplpy.DataFrame(index=["i"], columns=["rhspen"]))
        z.set_suffix("rhspen", pd.Series([], dtype=float))
        z.set_values(pd.Series([], dtype=float))
        z.set_values({})
        p.set_values(pd.Series([], dtype=float))
        p.set_values({})
        self.assertEqual(ampl.get_value("1+1"), 2)
        # Non-empty data on the same session still works afterwards.
        ampl.set["E"] = [1, 2]
        c.set_suffix("rhspen", pd.Series([3.0, 4.0], index=[1, 2]))
        self.assertEqual(ampl.get_value("c[2].rhspen"), 4)
        # Empty data assigns nothing: existing values are kept.
        c.set_suffix("rhspen", pd.Series([], dtype=float))
        self.assertEqual(ampl.get_value("c[2].rhspen"), 4)

    def test_empty_data_assignment_arity(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval(
            """
            set E default {};
            var x;
            var w {E, E};
            subject to c2 {i in E, j in E}: w[i, j] <= 1;
            suffix rhspen IN;
            let x := 5;
        """
        )
        x = ampl.get_variable("x")
        w = ampl.get_variable("w")
        c2 = ampl.get_constraint("c2")
        empty2 = pd.MultiIndex.from_tuples([], names=["i", "j"])
        empty3 = pd.MultiIndex.from_tuples([], names=["i", "j", "k"])
        # Empty data with matching arity is a no-op.
        c2.set_suffix("rhspen", pd.Series([], dtype=float, index=empty2))
        c2.set_suffix("rhspen", pd.DataFrame({"rhspen": []}, index=empty2))
        c2.set_suffix("rhspen", pd.Series([], dtype=float))  # stacked to 2-D
        c2.set_suffix(
            "rhspen", amplpy.DataFrame(index=["i", "j"], columns=["rhspen"])
        )
        w.set_values(pd.Series([], dtype=float, index=empty2))
        w.set_values(amplpy.DataFrame(index=["i", "j"], columns=["w"]))
        x.set_values(amplpy.DataFrame(index=[], columns=["x"]))
        # An empty flat index or dict states no index arity: nothing to
        # assign, for scalar and indexed entities alike.
        x.set_values(pd.Series([], dtype=float))
        x.set_values({})
        self.assertEqual(x.value(), 5)
        # Data of the wrong arity is rejected with the same error whether or
        # not it has rows.
        for call in [
            lambda: c2.set_suffix("rhspen", pd.Series([], dtype=float, index=empty3)),
            lambda: c2.set_suffix(
                "rhspen", amplpy.DataFrame(index=["i"], columns=["rhspen"])
            ),
            lambda: w.set_values(amplpy.DataFrame(index=["i"], columns=["w"])),
            lambda: w.set_values(
                amplpy.DataFrame(index=[("i", ["a"])], columns=[("w", [1.0])])
            ),
            lambda: c2.set_suffix(
                "rhspen", pd.Series([1.0], index=pd.MultiIndex.from_tuples([(1, 2, 3)]))
            ),
            lambda: x.set_values({"a": 1}),
            lambda: x.set_values(pd.Series([1.0], index=["a"])),
        ]:
            with self.assertRaises(ValueError):
                call()
        self.assertEqual(x.value(), 5)
        self.assertEqual(ampl.get_value("1+1"), 2)

    def test_empty_data_tuple_keys(self):
        if pd is None:
            self.skipTest("pandas not available")
        ampl = self.ampl
        ampl.eval(
            """
            set I := 1..2;
            var w {I, I, I} := 0;
            suffix rhspen IN;
        """
        )
        w = ampl.get_variable("w")
        keys = [(i, j, k) for i in [1, 2] for j in [1, 2] for k in [1, 2]]
        for cond in [lambda key: key == (1, 2, 1), lambda key: False]:
            # The same code path must work when the filter keeps no keys.
            data = pd.Series({key: 7.0 for key in keys if cond(key)}, dtype=float)
            w.set_values(data)
            w.set_suffix("rhspen", data)
        self.assertEqual(w[1, 2, 1].value(), 7)
        self.assertEqual(ampl.get_value("w[1, 2, 1].rhspen"), 7)
        self.assertEqual(ampl.get_value("sum {i in I, j in I, k in I} w[i, j, k]"), 7)

    def test_dataframe_without_native_data(self):
        ampl = self.ampl
        ampl.eval(
            """
            set S;
            var x;
            subject to c: x <= 1;
            suffix rhspen IN;
        """
        )
        x = ampl.get_variable("x")
        c = ampl.get_constraint("c")
        for make in [lambda: amplpy.DataFrame(None), lambda: amplpy.DataFrame(index=None)]:
            for call in [
                lambda: x.set_values(make()),
                lambda: c.set_suffix("rhspen", make()),
                lambda: ampl.set_data(make()),
                lambda: ampl.get_set("S").set_values(make()),
            ]:
                with self.assertRaises(ValueError):
                    call()
        self.assertEqual(ampl.get_value("1+1"), 2)

    def test_scalar_set_suffix_dataframe(self):
        # A DataFrame without index columns passes the indexarity check of a
        # scalar entity, but AMPL_EntitySetSuffixes would emit
        # "let y := 4", assigning the value instead of the suffix.
        ampl = self.ampl
        ampl.eval(
            """
            var y := 1;
            subject to c: y <= 10;
            suffix rhspen IN;
        """
        )
        for name, suffix in [("y", "relax"), ("c", "rhspen")]:
            entity = ampl.get_entity(name)
            with self.assertRaises(ValueError):
                entity.set_suffix(
                    suffix, amplpy.DataFrame(index=[], columns=[(suffix, [4])])
                )
            # Zero rows assign nothing, as for indexed entities.
            entity.set_suffix(suffix, amplpy.DataFrame(index=[], columns=[suffix]))
            entity.set_suffix(suffix, 4)
            self.assertEqual(ampl.get_value(f"{name}.{suffix}"), 4)
        self.assertEqual(ampl.get_variable("y").value(), 1)

    def test_empty_data_other_paths(self):
        # These paths hand zero rows to AMPL, which handles them: an empty set
        # assignment empties the set, and parameters are left unchanged.
        ampl = self.ampl
        ampl.eval(
            """
            set U;
            set U2 dimen 2;
            set S := {'a', 'b'};
            param r {S};
            param q {S, S} default 0;
            let r['a'] := 4;
        """
        )
        u, u2 = ampl.get_set("U"), ampl.get_set("U2")
        r, q = ampl.get_parameter("r"), ampl.get_parameter("q")
        for empty in [[], (), (v for v in [])] + ([np.array([])] if np else []):
            r.set_values(empty)
        if np is not None:
            q.set_values(np.zeros((0, 0)))
        self.assertEqual(r.to_dict(), {"a": 4})
        for assign, target in [
            (lambda: u.set_values([]), u),
            (lambda: u.set_values(amplpy.DataFrame(index=["U"])), u),
            (lambda: ampl.set_data(amplpy.DataFrame(index=["U"]), "U"), u),
            (lambda: u2.set_values([]), u2),
            (lambda: u2.set_values(amplpy.DataFrame(index=["i", "j"])), u2),
        ]:
            target.set_values([("x", "y")] if target is u2 else ["x"])
            self.assertEqual(target.size(), 1)
            assign()
            self.assertEqual(target.size(), 0)
        if pd is not None:
            ampl.set_data(pd.DataFrame({"r": []}))
            u.set_values(["x"])
            ampl.set_data(pd.DataFrame({"r": []}, index=pd.Index([], name="U")), "U")
            self.assertEqual(u.size(), 0)
        self.assertEqual(r.to_dict(), {"a": 4})
        self.assertEqual(ampl.get_value("1+1"), 2)

    def test_current_objective_indexed(self):
        ampl = self.ampl
        ampl.eval(
            """
            set S := {'a', 'b c', "it's"};
            set N := {1, 2.5};
            var x >= 1;
            maximize F {i in N}: i*x;
            minimize G {s in S, i in N}: x + i;
            minimize H: 7*x;
            let x := 1;
        """
        )
        for cmd, name, value, minimize in [
            ("objective F[2.5];", "F", 2.5, False),
            ("objective F[1];", "F", 1, False),
            ("objective G['b c', 1];", "G", 2, True),
            ("""objective G["it's", 2.5];""", "G", 3.5, True),
            ("objective H;", "H", 7, True),
        ]:
            ampl.eval(cmd)
            obj = ampl.get_current_objective()
            self.assertEqual(obj.name(), name)
            self.assertEqual(obj.value(), value)
            self.assertEqual(obj.minimization(), minimize)

    def test_indexed_entity_scalar_access(self):
        ampl = self.ampl
        # A single-instance family is the case in which the interpreter
        # would otherwise return the indexing key instead of the suffix value.
        for members in ["{'a'}", "{'a', 'b'}"]:
            ampl.reset()
            ampl.eval(
                f"""
                set S := {members};
                var x >= 1;
                var y {{S}} >= 0;
                minimize Obj {{s in S}}: 2*x;
                s.t. C {{s in S}}: y[s] <= 4;
                let x := 1;
            """
            )
            obj = ampl.get_objective("Obj")
            y = ampl.get_variable("y")
            c = ampl.get_constraint("C")
            for getter in [
                obj.value,
                obj.astatus,
                obj.exitcode,
                y.value,
                y.lb,
                y.astatus,
                y.defeqn,
                c.body,
                c.dual,
                c.ub,
                c.astatus,
                c.defvar,
            ]:
                with self.assertRaises(TypeError):
                    getter()
            # The sense belongs to the whole indexed objective.
            self.assertTrue(obj.minimization())
            self.assertEqual(obj["a"].value(), 2)
            self.assertTrue(obj["a"].minimization())
            self.assertEqual(y["a"].value(), 0)
            self.assertEqual(y["a"].lb(), 0)
            self.assertEqual(c["a"].ub(), 4)
            self.assertEqual(ampl.get_variable("x").value(), 1)
            ampl.eval("objective Obj['a'];")
            self.assertEqual(ampl.get_current_objective().value(), 2)

    def test_indexed_entity_scalar_setters(self):
        ampl = self.ampl
        ampl.eval(
            """
            set S := {'a', 'b'};
            var x;
            var y {S} >= 0;
            s.t. C {s in S}: y[s] <= 4;
            param p {S} default 5;
            param q := 3;
        """
        )
        y = ampl.get_variable("y")
        c = ampl.get_constraint("C")
        p = ampl.get_parameter("p")
        # These never worked on an indexed entity: AMPL rejected the
        # generated statement (e.g. "let y := 1;") with a RuntimeError.
        for setter in [
            lambda: y.set_value(1),
            lambda: y.fix(1),
            lambda: c.set_dual(1),
            lambda: ampl.var.__setitem__("y", 1),
            lambda: ampl.con.__setitem__("C", 1),
            p.value,
        ]:
            with self.assertRaises(TypeError):
                setter()
        self.assertEqual(y.get_values().to_dict(), {"a": 0, "b": 0})
        # Whole-family operations remain valid on indexed entities.
        y.fix()
        self.assertEqual(y["a"].astatus(), "fix")
        y.unfix()
        self.assertEqual(y["a"].astatus(), "unused")
        c.drop()
        self.assertEqual(c["a"].astatus(), "drop")
        c.restore()
        # Instances and scalar entities are unaffected.
        y["a"].set_value(2)
        self.assertEqual(y["a"].value(), 2)
        y["b"].fix(3)
        self.assertEqual(y["b"].value(), 3)
        self.assertEqual(p["a"], 5)
        self.assertEqual(p.get("a"), 5)
        self.assertEqual(ampl.get_parameter("q").value(), 3)
        ampl.get_variable("x").set_value(4)
        self.assertEqual(ampl.get_variable("x").value(), 4)

    def test_indexed_objective_minimization(self):
        ampl = self.ampl
        ampl.eval(
            """
            set I := 1..2;
            set E := {};
            var y;
            maximize G {i in I}: y;
            minimize H {i in I, j in I}: y + i;
            minimize Z {i in E}: y;
            maximize S: y;
        """
        )
        self.assertFalse(ampl.get_objective("G").minimization())
        self.assertFalse(ampl.get_objective("G")[1].minimization())
        self.assertTrue(ampl.get_objective("H").minimization())
        self.assertTrue(ampl.get_objective("H")[1, 2].minimization())
        self.assertTrue(ampl.get_objective("Z").minimization())
        self.assertFalse(ampl.get_objective("S").minimization())
        G = ampl.get_objective("G")
        ampl.eval("redeclare minimize G {i in I}: 2*y;")
        self.assertTrue(G.minimization())

    def test_current_objective_numeric_members(self):
        ampl = self.ampl
        ampl.eval(
            """
            set N := {1/3, 123456789.123456789, 1e20, -3, 2^60 + 1};
            set S := {'a', "it's, [x]"};
            var x >= 1;
            maximize F {n in N}: x + n;
            minimize G {s in S, n in N}: x + n;
            let x := 1;
        """
        )
        for cmd, expression in [
            ("objective F[1/3];", "F[1/3]"),
            ("objective F[123456789.123456789];", "F[123456789.123456789]"),
            ("objective F[1e20];", "F[1e20]"),
            ("objective F[-3];", "F[-3]"),
            ("objective F[2^60 + 1];", "F[2^60 + 1]"),
            ("""objective G["it's, [x]", 1/3];""", """G["it's, [x]", 1/3]"""),
            ("objective G['a', -3];", "G['a', -3]"),
        ]:
            ampl.eval(cmd)
            obj = ampl.get_current_objective()
            self.assertEqual(obj.value(), ampl.get_value(expression), cmd)

    def test_parse_ampl_subscript(self):
        from amplpy.ampl import _parse_ampl_subscript as parse

        self.assertEqual(parse("'a'"), ["a"])
        self.assertEqual(parse("'a',1"), ["a", 1])
        self.assertEqual(parse(" 'a' , 1 "), ["a", 1])
        self.assertEqual(parse("1,'a',2.5"), [1, "a", 2.5])
        self.assertEqual(parse("\"it's, [x]\",'say \"hi\"'"), ["it's, [x]", 'say "hi"'])
        self.assertEqual(parse("'it''s'"), ["it's"])
        self.assertEqual(parse("\"a\"\"b\""), ['a"b'])
        self.assertEqual(parse("''"), [""])
        self.assertEqual(parse("0.3333333333333333"), [1 / 3])
        self.assertEqual(parse("-3"), [-3])
        self.assertEqual(parse("+4"), [4])
        self.assertEqual(parse(".5"), [0.5])
        self.assertEqual(parse("1e-30"), [1e-30])
        # Integral values are returned as int only while exactly representable.
        self.assertIsInstance(parse("2")[0], int)
        self.assertIsInstance(parse("1e+20")[0], float)
        self.assertEqual(parse("1e+20"), [1e20])
        # AMPL prints infinite members as Infinity and -Infinity.
        self.assertEqual(parse("Infinity,-Infinity"), [float("inf"), float("-inf")])
        # Only AMPL number syntax is numeric; other unquoted items stay strings.
        self.assertEqual(parse("alpha"), ["alpha"])
        self.assertEqual(parse("nan,inf,1_0"), ["nan", "inf", "1_0"])
        for invalid in [
            "'a",
            "'a'b",
            "'a' 'b'",
            "1,",
            ",1",
            "1,,2",
            "",
            "1 2",
            "a b",
            "a'b",
            "'a',1 2",
        ]:
            with self.assertRaises(ValueError, msg=invalid):
                parse(invalid)

    def test_current_objective_infinite_members(self):
        ampl = self.ampl
        ampl.eval(
            """
            set N := {Infinity, -Infinity, 1};
            var x >= 1;
            maximize F {n in N}: x;
            minimize G {s in {'a'}, n in N}: 2*x;
            let x := 1;
        """
        )
        for cmd, expected in [
            ("objective F[Infinity];", "F[Infinity]"),
            ("objective F[-Infinity];", "F[-Infinity]"),
            ("objective G['a', Infinity];", "G['a',Infinity]"),
        ]:
            ampl.eval(cmd)
            obj = ampl.get_current_objective()
            self.assertIn(expected, obj.expand().replace(" ", ""), cmd)
            self.assertEqual(obj.value(), ampl.get_value(cmd[10:-1]))

    def test_current_objective_unresolved(self):
        import amplpy.ampl as ampl_module

        ampl = self.ampl
        ampl.eval(
            """
            set N := {1, 2};
            var x >= 1;
            maximize F {n in N}: x + n;
            objective F[2];
            let x := 1;
        """
        )
        self.assertEqual(ampl.get_current_objective().value(), 3)
        # An index that is not a member of the indexing set (as would result
        # from a parsing mismatch) must be reported as KeyError.
        parse = ampl_module._parse_ampl_subscript
        try:
            ampl_module._parse_ampl_subscript = lambda subscript: [7]
            with self.assertRaises(KeyError):
                ampl.get_current_objective()
        finally:
            ampl_module._parse_ampl_subscript = parse
        self.assertEqual(ampl.get_current_objective().value(), 3)

    def test_scalar_check_after_redeclaration(self):
        ampl = self.ampl
        ampl.eval("var x := 3;")
        x = ampl.get_variable("x")
        self.assertEqual(x.value(), 3)
        # The same object must notice that x is now indexed.
        ampl.reset()
        ampl.eval("set S := {'a'}; var x {S} := 1;")
        with self.assertRaises(TypeError):
            x.value()
        self.assertEqual(x["a"].value(), 1)
        ampl.reset()
        ampl.eval("var x := 5;")
        self.assertEqual(x.value(), 5)

    def test_parameter_instances(self):
        ampl = self.ampl
        for members in ["{'a'}", "{'a', 'b'}"]:
            ampl.reset()
            ampl.eval(
                f"""
                set S := {members};
                param p {{S}};
                param q {{S}} symbolic;
                let {{s in S}} p[s] := if s = 'a' then 10 else 20;
                let {{s in S}} q[s] := s & s;
            """
            )
            p = ampl.get_parameter("p")
            q = ampl.get_parameter("q")
            for (key,), instance in p:
                self.assertEqual(instance.value(), p[key])
            for (key,), instance in q:
                self.assertEqual(instance.value(), key + key)
            for (key,), instance in p:
                instance.set(7 if key == "a" else 8)
            for (key,), instance in q:
                instance.set("z" + key)
            self.assertEqual(p["a"], 7)
            self.assertEqual(q["a"], "za")
            if members == "{'a', 'b'}":
                self.assertEqual(p["b"], 8)
                self.assertEqual(q["b"], "zb")
            with self.assertRaises(TypeError):
                p.set(9)
            with self.assertRaises(TypeError):
                q.set("z")
            self.assertEqual(p["a"], 7)
            # Plain entities resolve parameter instances to their values too.
            self.assertEqual(ampl.get_entity("p").get("a"), 7)
            self.assertEqual(p.get("a"), 7)
            self.assertEqual(p.get(["a"]), 7)

    def test_indexed_entity_get_and_suffix(self):
        ampl = self.ampl
        ampl.eval(
            """
            set S := {'a'};
            var y {S} := 1;
            var z := 2;
        """
        )
        y = ampl.get_variable("y")
        z = ampl.get_variable("z")
        # get() without an index returns the indexed entity itself.
        self.assertIs(y.get(), y)
        with self.assertRaises(TypeError):
            y.get().value()
        self.assertEqual(y.get("a").value(), 1)
        self.assertEqual(z.get().value(), 2)
        # A single suffix value can only be assigned to a scalar or instance.
        for value in [1, "s"]:
            with self.assertRaises(TypeError):
                y.set_suffix("relax", value)
        y["a"].set_suffix("relax", 1)
        self.assertEqual(ampl.get_value("y['a'].relax"), 1)
        z.set_suffix("relax", 1)
        self.assertEqual(ampl.get_value("z.relax"), 1)

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
