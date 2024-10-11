#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os
from .. import modules


class TestBase(unittest.TestCase):
    def setUp(self):
        modules.uninstall()

    def get_env_path(self):
        return os.environ.get("PATH", "")

    def get_env_path_list(self):
        return self.get_env_path().split(os.pathsep)

    def tearDown(self):
        modules.uninstall()


if __name__ == "__main__":
    unittest.main()
