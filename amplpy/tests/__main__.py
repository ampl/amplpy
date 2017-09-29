#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest
from .test_ampl import TestAMPL
from .test_entities import TestEntities
from .test_iterators import TestIterators
from .test_dataframe import TestDataFrame
from .test_environment import TestEnvironment
from .test_properties import TestProperties


if __name__ == '__main__':
    unittest.main()
