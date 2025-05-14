#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from . import TestBase
import amplpy


class TestOutputHandler(TestBase.TestBase):
    """Test OutputHandlers."""

    def test_output_kind(self):
        ampl = self.ampl
        class LastOutput(amplpy.OutputHandler):
            def __init__(self):
                self.lastkind = None
                super(LastOutput, self).__init__()

            def output(self, kind, msg):
                self.lastkind = kind

            def getLastKind(self):
                return self.lastkind

        output_handler = LastOutput()
        ampl.set_output_handler(output_handler)
        ampl.eval("print '1';")
        self.assertEqual(output_handler.getLastKind(), amplpy.Kind.PRINT)
        ampl.eval("printf '1';")
        self.assertEqual(output_handler.getLastKind(), amplpy.Kind.PRINTF)
        ampl.eval("var x; display x;")
        self.assertEqual(output_handler.getLastKind(), amplpy.Kind.DISPLAY)
        ampl.eval("show x;")
        self.assertEqual(output_handler.getLastKind(), amplpy.Kind.SHOW)
        ampl.eval("solve;")
        self.assertEqual(output_handler.getLastKind(), amplpy.Kind.SOLVE)


if __name__ == "__main__":
    unittest.main()
