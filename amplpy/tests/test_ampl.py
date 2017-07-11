#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import

from . import TestBase
import unittest
import amplpy
import os


class TestAMPL(TestBase.TestBase):
    """Test AMPL."""

    def testAMPL(self):
        from amplpy import Set, Parameter, Variable, Constraint, Objective
        ampl = self.ampl
        self.assertEqual(ampl.getData('1..3').getNumRows(), 3)
        self.assertEqual(ampl.getData('1..3').getNumCols(), 1)
        # self.assertEqual(ampl.getData('1..3', '1..3').getNumCols(), 2)# FIXME
        ampl.eval('set X := 1..10;')
        self.assertTrue(isinstance(ampl.getEntity('X'), amplpy.Entity))
        self.assertEqual(ampl.getEntity('X').getValues().getNumRows(), 10)
        self.assertEqual(ampl.getData('X').getNumRows(), 10)
        with self.assertRaises(RuntimeError):
            self.assertRaises(ampl.getData('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getEntity('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getSet('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getParameter('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getVariable('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getConstraint('XXX'))
        with self.assertRaises(ValueError):
            self.assertRaises(ampl.getObjective('XXX'))
        ampl.reset()  # FIXME: seems to have no efect after eval()
        ampl.eval('set _s; param _p; var _v; s.t. _c: _v = 0; maximize _o: 0;')
        self.assertTrue(isinstance(ampl.getSet('_s'), Set))
        self.assertTrue(isinstance(ampl.getParameter('_p'), Parameter))
        self.assertTrue(isinstance(ampl.getVariable('_v'), Variable))
        self.assertTrue(isinstance(ampl.getConstraint('_c'), Constraint))
        self.assertTrue(isinstance(ampl.getObjective('_o'), Objective))
        print(list(ampl.getSets()))
        # self.assertEqual(len(ampl.getSets()), 1) # FIXME: 2 != 1
        self.assertEqual(len(ampl.getParameters()), 1)
        self.assertEqual(len(ampl.getVariables()), 1)
        self.assertEqual(len(ampl.getConstraints()), 1)
        self.assertEqual(len(ampl.getObjectives()), 1)
        ampl.reset()
        with self.assertRaises(RuntimeError):
            ampl.eval('X')
        self.assertTrue(ampl.isRunning())
        self.assertFalse(ampl.isBusy())

    def testPath(self):
        ampl = self.ampl
        self.assertEqual(
            os.path.abspath(ampl.cd()),
            os.path.abspath(os.curdir)
        )
        ampl.cd('..')
        self.assertEqual(
            os.path.abspath(ampl.cd()),
            os.path.abspath(os.path.join(os.curdir, '..'))
        )

    def testOptions(self):
        ampl = self.ampl
        ampl.setOption('a', 's')
        ampl.setOption('b', 123)
        ampl.setOption('c', 1.23)
        ampl.setOption('d', True)
        with self.assertRaises(TypeError):
            ampl.setOption('e', None)
        self.assertEqual(ampl.getOption('a'), 's')
        self.assertEqual(ampl.getOption('b'), 123)
        self.assertEqual(ampl.getOption('c'), 1.23)
        self.assertEqual(ampl.getOption('d'), True)

    def testHandlers(self):
        from time import sleep
        ampl = self.ampl

        class MyOutputHandler(amplpy.OutputHandler):
            def __init__(self):
                self.lastmsg = None

            def output(self, kind, msg):
                if kind == amplpy.Kind.DISPLAY:
                    print('Display: |{}|'.format(msg))
                self.lastmsg = msg

        class MyErrorHandler(amplpy.ErrorHandler):
            def __init__(self):
                self.lastError = None
                self.lastWarning = None

            def error(self, exception):
                print(type(exception))
                print('Error:', exception.getMessage())
                self.lastError = exception

            def warning(self, exception):
                print(type(exception))
                print('Warning:', exception.getMessage())
                self.lastWarning = exception

        outputHandler = MyOutputHandler()
        ampl.setOutputHandler(outputHandler)
        errorHandler = MyErrorHandler()
        ampl.setErrorHandler(errorHandler)
        self.assertEqual(ampl.getOutputHandler(), outputHandler)
        self.assertEqual(ampl.getErrorHandler(), errorHandler)
        ampl.display('1', '2', '3')
        self.assertTrue('1 = 1' in outputHandler.lastmsg)
        self.assertTrue('2 = 2' in outputHandler.lastmsg)
        self.assertTrue('3 = 3' in outputHandler.lastmsg)
        ampl.eval('display X;')
        self.assertEqual(
            str(errorHandler.lastWarning.getMessage()),
            'X is not defined'
        )
        ampl.eval('diy X;')
        self.assertEqual(
            str(errorHandler.lastError.getMessage()),
            'syntax error'
        )
        self.assertTrue(
            isinstance(errorHandler.lastWarning.getSourceName(), basestring)
        )
        self.assertTrue(
            isinstance(errorHandler.lastWarning.getLineNumber(), int)
        )
        self.assertTrue(
            isinstance(errorHandler.lastWarning.getOffset(), int)
        )
        self.assertTrue(
            isinstance(errorHandler.lastWarning.getMessage(), basestring)
        )


if __name__ == '__main__':
    unittest.main()
