#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from .test_ampl import TestAMPL
from .test_entities import TestEntities
from .test_exceptions import TestExceptions
from .test_iterators import TestIterators
from .test_dataframe import TestDataFrame
from .test_environment import TestEnvironment
from .test_outputhandler import TestOutputHandler
from .test_properties import TestProperties


if __name__ == "__main__":
    unittest.main()
