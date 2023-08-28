#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import amplpy


class TestExamples(unittest.TestCase):
    """Test examples."""

    def test_first_example(self):
        import first_example

        first_example.main(1, [None])

    def test_options_example(self):
        import options_example

        options_example.main(1, [None])

    def test_dataframe_example(self):
        import dataframe_example

        dataframe_example.main(1, [None])

    def test_multidimensional_example(self):
        import multidimensional_example

        multidimensional_example.main(1, [None])

    def test_dietmodel_example(self):
        import diet_model

        diet_model.main(1, [None])

    def test_efficient_frontier_example(self):
        import efficient_frontier

        efficient_frontier.main(1, [None])

    def test_trackingmodel_example(self):
        import tracking_model

        tracking_model.main(1, [None])

    def test_location_transportation(self):
        import location_transportation

        location_transportation.main(1, [None])


if __name__ == "__main__":
    unittest.main()
