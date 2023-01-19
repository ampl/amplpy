#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
import unittest
import os

# from builtins import map, range, object, zip, sorted
from past.builtins import basestring

import amplpy
from . import TestBase


class TestAMPL(TestBase.TestBase):
    """Test AMPL."""

    def test_ampl(self):
        from amplpy import Set, Parameter, Variable, Constraint, Objective

        ampl = self.ampl
        self.assertEqual(ampl.get_data("1..3").get_num_rows(), 3)
        self.assertEqual(ampl.get_data("1..3").get_num_cols(), 1)
        ampl.eval("set X := 1..10;")
        self.assertTrue(isinstance(ampl.get_entity("X"), amplpy.Entity))
        self.assertEqual(ampl.get_entity("X").get_values().get_num_rows(), 10)
        self.assertEqual(ampl.get_data("X").get_num_rows(), 10)

        with self.assertRaises(RuntimeError):
            self.assertRaises(ampl.get_data("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_entity("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_set("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_parameter("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_variable("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_constraint("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.get_objective("XXX"))
        self.assertEqual(len(ampl.get_sets()), 1)
        ampl.reset()
        self.assertEqual(len(ampl.get_sets()), 0)
        ampl.eval("set _s; param _p; var _v; s.t. _c: _v = 0; maximize _o: 0;")
        self.assertTrue(isinstance(ampl.get_set("_s"), Set))
        self.assertTrue(isinstance(ampl.get_parameter("_p"), Parameter))
        self.assertTrue(isinstance(ampl.get_variable("_v"), Variable))
        self.assertTrue(isinstance(ampl.get_constraint("_c"), Constraint))
        self.assertTrue(isinstance(ampl.get_objective("_o"), Objective))
        self.assertEqual(len(ampl.get_sets()), 1)
        self.assertEqual(len(ampl.get_parameters()), 1)
        self.assertEqual(len(ampl.get_variables()), 1)
        self.assertEqual(len(ampl.get_constraints()), 1)
        self.assertEqual(len(ampl.get_objectives()), 1)
        ampl.reset()
        with self.assertRaises(ValueError):
            ampl.eval("X")
        self.assertTrue(ampl.is_running())
        self.assertFalse(ampl.is_busy())

    def test_getdata_multi(self):
        ampl = self.ampl
        ampl.eval(
            """
        param p1{i in 1..10} := 1*i;
        param p2{i in 1..10} := 2*i;
        param p3{i in 0..10: i >= 1} := 3*i;
        """
        )
        df = ampl.get_data("p1", "p2", "p3")
        df = ampl.get_data("p1", "p2", "p3")
        self.assertEqual(list(df.get_column("p1")), [i for i in range(1, 10 + 1)])
        self.assertEqual(list(df.get_column("p2")), [2 * i for i in range(1, 10 + 1)])
        self.assertEqual(list(df.get_column("p3")), [3 * i for i in range(1, 10 + 1)])
        self.assertEqual(df.get_headers(), ("index0", "p1", "p2", "p3"))
        df = ampl.get_data("1..10", "p1", "p2", "p3")
        self.assertEqual(list(df.get_column("p1")), [i for i in range(1, 10 + 1)])
        self.assertEqual(list(df.get_column("p2")), [2 * i for i in range(1, 10 + 1)])
        self.assertEqual(list(df.get_column("p3")), [3 * i for i in range(1, 10 + 1)])
        self.assertEqual(df.get_headers(), ("1 .. 10", "p1", "p2", "p3"))
        with self.assertRaises(TypeError):
            ampl.get_data("1..11", "p1", "p2", "p3")

    def test_path(self):
        ampl = self.ampl
        self.assertEqual(os.path.abspath(ampl.cd()), os.path.abspath(os.curdir))
        ampl.cd("..")
        self.assertEqual(
            os.path.abspath(ampl.cd()), os.path.abspath(os.path.join(os.curdir, ".."))
        )

    def test_options(self):
        ampl = self.ampl
        ampl.set_option("a", "s")
        ampl.set_option("b", 123)
        ampl.set_option("c", 1.23)
        ampl.set_option("d", True)
        with self.assertRaises(TypeError):
            ampl.set_option("e", None)
        self.assertEqual(ampl.get_option("a"), "s")
        self.assertEqual(ampl.get_option("b"), 123)
        self.assertEqual(ampl.get_option("c"), 1.23)
        self.assertEqual(ampl.get_option("d"), True)

    def test_handlers(self):
        ampl = self.ampl

        class MyOutputHandler(amplpy.OutputHandler):
            def __init__(self):
                self.lastmsg = None
                super(MyOutputHandler, self).__init__()

            def output(self, kind, msg):
                if kind == amplpy.Kind.DISPLAY:
                    print("Display: |{}|".format(msg))
                self.lastmsg = msg

        class MyErrorHandler(amplpy.ErrorHandler):
            def __init__(self):
                self.last_wrror = None
                self.last_warning = None

            def error(self, exception):
                print(type(exception))
                print("Error:", exception.get_message())
                self.last_error = exception

            def warning(self, exception):
                print(type(exception))
                print("Warning:", exception.get_message())
                self.last_warning = exception

            def check(self):
                pass

        output_handler = MyOutputHandler()
        ampl.set_output_handler(output_handler)
        error_handler = MyErrorHandler()
        ampl.set_error_handler(error_handler)
        self.assertEqual(ampl.get_output_handler(), output_handler)
        self.assertEqual(ampl.get_error_handler(), error_handler)
        ampl.display("1", "2", "3")
        self.assertTrue("1 = 1" in output_handler.lastmsg)
        self.assertTrue("2 = 2" in output_handler.lastmsg)
        self.assertTrue("3 = 3" in output_handler.lastmsg)
        ampl.eval("display X;")
        self.assertTrue(
            error_handler.last_warning.get_message().startswith("X is not defined")
        )
        ampl.eval("diy X;")
        self.assertTrue(
            error_handler.last_error.get_message().startswith("syntax error")
        )
        self.assertTrue(
            isinstance(error_handler.last_warning.get_source_name(), basestring)
        )
        self.assertTrue(isinstance(error_handler.last_warning.get_line_number(), int))
        self.assertTrue(isinstance(error_handler.last_warning.get_offset(), int))
        self.assertTrue(
            isinstance(error_handler.last_warning.get_message(), basestring)
        )

    def test_empty_handlers(self):
        ampl = self.ampl
        callback = amplpy.Runnable()
        output_handler = amplpy.OutputHandler()
        error_handler = amplpy.ErrorHandler()
        ampl.set_output_handler(output_handler)
        ampl.set_error_handler(error_handler)
        ampl.eval_async("display 1;", callback)
        ampl.wait()

    def test_broken_handlers(self):
        ampl = self.ampl

        class OutputHandlerRaise(amplpy.OutputHandler):
            def output(self, kind, msg):
                assert False

        class ErrorHandlerIgnore(amplpy.ErrorHandler):
            def error(self, exception):
                assert True

            def warning(self, exception):
                assert True

        class ErrorHandlerRaise(amplpy.ErrorHandler):
            def error(self, exception):
                raise RuntimeError("failed")

            def warning(self, exception):
                raise RuntimeError("failed")

        with self.assertRaises(amplpy.AMPLException):
            ampl.eval("X X;")

        error_handler_ignore = ErrorHandlerIgnore()
        ampl.set_error_handler(error_handler_ignore)
        ampl.eval("X X;")

        error_handler_raise = ErrorHandlerRaise()
        ampl.set_error_handler(error_handler_raise)
        with self.assertRaises(RuntimeError):
            ampl.eval("X X;")

        ampl.set_output_handler(OutputHandlerRaise())
        with self.assertRaises(RuntimeError):
            ampl.eval("display 1;")

    def test_async(self):
        from threading import Lock

        ampl = self.ampl

        class MyOutputHandler(amplpy.OutputHandler):
            def output(self, kind, msg):
                pass

        class MyErrorHandler(amplpy.ErrorHandler):
            def __init__(self, mutex1, mutex2):
                self.mutex1 = mutex1
                self.mutex2 = mutex2

            def error(self, exception):
                try:
                    self.mutex1.release()
                except Exception:
                    pass
                try:
                    self.mutex2.release()
                except Exception:
                    pass
                raise exception

            def warning(self, exception):
                print("Warning:", exception.get_message())

        class Callback(amplpy.Runnable):
            def __init__(self, mutex1, mutex2):
                self.ready = False
                self.mutex1 = mutex1
                self.mutex2 = mutex2
                super(Callback, self).__init__()

            def run(self):
                self.mutex2.acquire()
                self.ready = True
                self.mutex1.release()
                self.mutex2.release()

        model = self.str2file(
            "model.mod",
            """
            set X;
            set A := 1..10000000;
            param p{i in A} := i;
        """,
        )
        data = self.str2file(
            "data.dat",
            """
            set X := 1, 2, 3;
        """,
        )

        mutex1 = Lock()
        mutex2 = Lock()
        try:
            callback = Callback(mutex1, mutex2)
            output_handler = MyOutputHandler()
            ampl.set_output_handler(output_handler)
            error_handler = MyErrorHandler(mutex1, mutex2)
            ampl.set_error_handler(error_handler)

            mutex1.acquire()
            mutex2.acquire()
            callback.ready = False
            ampl.read_async(model, callback)
            self.assertFalse(callback.ready)
            mutex2.release()
            mutex1.acquire()
            self.assertTrue(callback.ready)

            mutex2.acquire()
            callback.ready = False
            ampl.read_data_async(data, callback)
            self.assertFalse(callback.ready)
            mutex2.release()
            mutex1.acquire()
            self.assertTrue(callback.ready)

            mutex2.acquire()
            callback.ready = False
            ampl.eval_async("display {i in A: i not in A};", callback)
            ampl.interrupt()
            self.assertFalse(callback.ready)
            mutex2.release()
            mutex1.acquire()
            self.assertTrue(callback.ready)
            self.assertFalse(ampl.is_busy())
            self.assertTrue(ampl.is_running())

        except Exception:
            mutex1.acquire(False)
            mutex1.release()
            mutex2.acquire(False)
            mutex2.release()
            raise

    def test_get_output(self):
        ampl = self.ampl
        self.assertEqual(ampl.get_output("display 5;"), "5 = 5\n\n")
        with self.assertRaises(ValueError):
            ampl.get_output("display 3")
        with self.assertRaises(ValueError):
            ampl.get_output("for {i in 1..10} {")
        self.assertEqual(ampl.get_output("display 5; display 1;"), "5 = 5\n\n1 = 1\n\n")

    def test_export(self):
        ampl = self.ampl
        model = self.str2file(
            "model.mod",
            """
            set A;
            set FLOOR;
            set family {FLOOR};
        """,
        )
        data = self.str2file(
            "data.dat",
            """
            set A := 1, 2, 3, 4;
            set FLOOR := 'first' 'second';
            set family['first'] := 'Gutierrez';
            set family['second'] := 'Montoro';
        """,
        )
        ampl.read(model)
        ampl.read_data(data)
        model2 = self.tmpfile("model2.mod")
        data2 = self.tmpfile("data2.dat")
        ampl.export_model(model2)
        ampl.export_data(data2)
        ampl.reset()
        ampl.read(model2)
        ampl.read_data(data2)
        self.assertEqual(
            ampl.set["family"]["first"].get_values().to_list(), ["Gutierrez"]
        )
        self.assertEqual(
            ampl.set["family"]["second"].get_values().to_list(), ["Montoro"]
        )
        self.assertEqual(ampl.set["A"].get_values().to_list(), [1, 2, 3, 4])

    def test_pathlib(self):
        ampl = self.ampl
        try:
            from pathlib import Path
        except ImportError:
            return
        model = self.str2file("model.mod", "set A := 1..10;")
        p = Path(model)
        ampl.read(p)
        ampl.display("A")


if __name__ == "__main__":
    unittest.main()
