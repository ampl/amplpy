#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from .test_preload import TestPreload as Test1
from .test_install import TestInstall as Test2
from .test_load import TestLoad as Test3
from .test_run import TestRun as Test4

if __name__ == "__main__":
    unittest.main()
