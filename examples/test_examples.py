#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

import unittest
import amplpy


class TestExamples(unittest.TestCase):
    """Test examples."""

    def testFirstExample(self):
        import firstexample
        firstexample.main(1, [None])

    def testOptionsExample(self):
        import optionsexample
        optionsexample.main(1, [None])

    def testAsyncExample(self):
        import asyncexample
        asyncexample.main(1, [None])

    def testDataFrameExample(self):
        import dataframeexample
        dataframeexample.main(1, [None])

    def testMultidimensionalExample(self):
        import multidimensionalexample
        multidimensionalexample.main(1, [None])

    def testDietModelExample(self):
        import dietmodel
        dietmodel.main(1, [None])

    def testEfficientFrontierExample(self):
        import efficientfrontier
        efficientfrontier.main(1, [None])

    def testTrackingModelExample(self):
        import trackingmodel
        trackingmodel.main(1, [None])


if __name__ == '__main__':
    unittest.main()
