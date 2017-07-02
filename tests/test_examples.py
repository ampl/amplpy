#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .context import amplpy
from examples import (
    firstexample,
    optionsexample,
    asyncexample,
    dataframeexample,
    multidimensionalexample,
    dietmodel,
    efficientfrontier,
    trackingmodel,
)
import unittest


class TestExamples(unittest.TestCase):
    """Test examples."""

    def testFirstExample(self):
        firstexample.main(1, [None])

    def testOptionsExample(self):
        optionsexample.main(1, [None])

    def testAsyncExample(self):
        # asyncexample.main(1, [None])
        pass

    def testDataFrameExample(self):
        dataframeexample.main(1, [None])

    def testMultidimensionalExample(self):
        multidimensionalexample.main(1, [None])

    def testDietModelExample(self):
        dietmodel.main(1, [None])

    def testEfficientFrontierExample(self):
        efficientfrontier.main(1, [None])

    def testTrackingModelExample(self):
        trackingmodel.main(1, [None])


if __name__ == '__main__':
    unittest.main()
