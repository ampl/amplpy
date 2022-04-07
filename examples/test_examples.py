#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

import unittest
import amplpy


class TestExamples(unittest.TestCase):
    """Test examples."""

    def test_first_example(self):
        import firstexample

        firstexample.main(1, [None])

    def test_options_example(self):
        import optionsexample

        optionsexample.main(1, [None])

    def test_async_example(self):
        import asyncexample

        asyncexample.main(1, [None])

    def test_dataframe_example(self):
        import dataframeexample

        dataframeexample.main(1, [None])

    def test_multidimensional_example(self):
        import multidimensionalexample

        multidimensionalexample.main(1, [None])

    def test_dietmodel_example(self):
        import dietmodel

        dietmodel.main(1, [None])

    def test_efficient_frontier_example(self):
        import efficientfrontier

        efficientfrontier.main(1, [None])

    def test_trackingmodel_example(self):
        import trackingmodel

        trackingmodel.main(1, [None])

    def test_location_transportation(self):
        import locationtransportation

        locationtransportation.main(1, [None])


if __name__ == "__main__":
    unittest.main()
