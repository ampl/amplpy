#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import TestBase
import unittest
import amplpy
import os


class TestAMPL(TestBase.TestBase):
    """Test AMPL."""

    def testAMPL(self):
        from amplpy import Set, Parameter, Variable, Constraint, Objective

        ampl = self.ampl
        self.assertEqual(ampl.getData("1..3")._getNumRows(), 3)
        self.assertEqual(ampl.getData("1..3")._getNumCols(), 1)
        ampl.eval("set X := 1..10;")
        self.assertTrue(isinstance(ampl.getEntity("X"), amplpy.Entity))
        self.assertEqual(ampl.getEntity("X").getValues()._getNumRows(), 10)
        self.assertEqual(ampl.getData("X")._getNumRows(), 10)

        with self.assertRaises(RuntimeError):
            self.assertRaises(ampl.getData("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getEntity("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getSet("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getParameter("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getVariable("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getConstraint("XXX"))
        with self.assertRaises(KeyError):
            self.assertRaises(ampl.getObjective("XXX"))
        ampl.reset()
        ampl.eval("set _s; param _p; var _v; s.t. _c: _v = 0; maximize _o: 0;")
        self.assertTrue(isinstance(ampl.getSet("_s"), Set))
        self.assertTrue(isinstance(ampl.getParameter("_p"), Parameter))
        self.assertTrue(isinstance(ampl.getVariable("_v"), Variable))
        self.assertTrue(isinstance(ampl.getConstraint("_c"), Constraint))
        self.assertTrue(isinstance(ampl.getObjective("_o"), Objective))
        print(list(ampl.getSets()))
        self.assertEqual(len(ampl.getSets()), 1)
        self.assertEqual(len(ampl.getParameters()), 1)
        self.assertEqual(len(ampl.getVariables()), 1)
        self.assertEqual(len(ampl.getConstraints()), 1)
        self.assertEqual(len(ampl.getObjectives()), 1)
        ampl.reset()
        with self.assertRaises(ValueError):
            ampl.eval("X")
        self.assertTrue(ampl.isRunning())

    def testPath(self):
        ampl = self.ampl
        self.assertEqual(os.path.abspath(ampl.cd()), os.path.abspath(os.curdir))
        ampl.cd("..")
        self.assertEqual(
            os.path.abspath(ampl.cd()), os.path.abspath(os.path.join(os.curdir, ".."))
        )

    def testOptions(self):
        ampl = self.ampl
        ampl.setOption("a", "s")
        ampl.setOption("b", 123)
        ampl.setOption("c", 1.23)
        ampl.setOption("d", True)
        with self.assertRaises(TypeError):
            ampl.setOption("e", None)
        self.assertEqual(ampl.getOption("a"), "s")
        self.assertEqual(ampl.getOption("b"), 123)
        self.assertEqual(ampl.getOption("c"), 1.23)
        self.assertEqual(ampl.getOption("d"), True)

    def testHandlers(self):
        from time import sleep

        ampl = self.ampl

        class MyOutputHandler(amplpy.OutputHandler):
            def __init__(self):
                self.lastmsg = None

            def output(self, kind, msg):
                if kind == amplpy.Kind.DISPLAY:
                    print(f"Display: |{msg}|")
                self.lastmsg = msg

        class MyErrorHandler(amplpy.ErrorHandler):
            def __init__(self):
                self.lastError = None
                self.lastWarning = None

            def error(self, exception):
                print(type(exception))
                print("Error:", exception.getMessage())
                self.lastError = exception

            def warning(self, exception):
                print(type(exception))
                print("Warning:", exception.getMessage())
                self.lastWarning = exception

            def check(self):
                pass

        outputHandler = MyOutputHandler()
        ampl.setOutputHandler(outputHandler)
        errorHandler = MyErrorHandler()
        ampl.setErrorHandler(errorHandler)
        self.assertEqual(ampl.getOutputHandler(), outputHandler)
        self.assertEqual(ampl.getErrorHandler(), errorHandler)
        ampl.display("1", "2", "3")
        self.assertTrue("1 = 1" in outputHandler.lastmsg)
        self.assertTrue("2 = 2" in outputHandler.lastmsg)
        self.assertTrue("3 = 3" in outputHandler.lastmsg)
        ampl.eval("display X;")
        self.assertTrue(
            errorHandler.lastWarning.getMessage().startswith("X is not defined")
        )
        ampl.eval("diy X;")
        self.assertTrue(errorHandler.lastError.getMessage().startswith("syntax error"))
        self.assertTrue(isinstance(errorHandler.lastWarning.getSourceName(), str))
        self.assertTrue(isinstance(errorHandler.lastWarning.getLineNumber(), int))
        self.assertTrue(isinstance(errorHandler.lastWarning.getOffset(), int))
        self.assertTrue(isinstance(errorHandler.lastWarning.getMessage(), str))

    def testEmptyHandlers(self):
        ampl = self.ampl
        outputHandler = amplpy.OutputHandler()
        errorHandler = amplpy.ErrorHandler()
        ampl.setOutputHandler(outputHandler)
        ampl.setErrorHandler(errorHandler)
        ampl.eval("display 1;")

    def testBrokenHandlers(self):
        ampl = self.ampl

        class MyOutputHandler(amplpy.OutputHandler):
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

        errorHandlerIgnore = ErrorHandlerIgnore()
        ampl.setErrorHandler(errorHandlerIgnore)
        ampl.eval("X X;")

        errorHandlerRaise = ErrorHandlerRaise()
        ampl.setErrorHandler(errorHandlerRaise)
        with self.assertRaises(RuntimeError):
            ampl.eval("X X;")

    def testGetOutput(self):
        ampl = self.ampl
        self.assertEqual(ampl.getOutput("display 5;"), "5 = 5\n\n")
        with self.assertRaises(ValueError):
            ampl.getOutput("display 3")
        with self.assertRaises(ValueError):
            ampl.getOutput("for {i in 1..10} {")
        self.assertEqual(ampl.getOutput("display 5; display 1;"), "5 = 5\n\n1 = 1\n\n")

    def testExport(self):
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
        ampl.readData(data)
        model2 = self.tmpfile("model2.mod")
        data2 = self.tmpfile("data2.dat")
        ampl.exportModel(model2)
        ampl.exportData(data2)
        ampl.reset()
        ampl.read(model2)
        ampl.readData(data2)
        self.assertEqual(
            ampl.set["family"]["first"].getValues().toList(), ["Gutierrez"]
        )
        self.assertEqual(ampl.set["family"]["second"].getValues().toList(), ["Montoro"])
        self.assertEqual(ampl.set["A"].getValues().toList(), [1, 2, 3, 4])

    def testPath(self):
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
