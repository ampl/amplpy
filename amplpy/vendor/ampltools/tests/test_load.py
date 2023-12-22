#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os

from .. import modules
from . import TestBase


class TestLoad(TestBase.TestBase):
    """Test ampltools.modules: load, unload, and path."""

    def test_load_verbose(self):
        self._test_load(verbose=True)

    def test_load_silent(self):
        self._test_load(verbose=False)

    def _test_load(self, verbose):
        self.assertEqual(modules.installed(), [])

        initial_path = self.get_env_path_list()

        self.assertEqual(modules.installed(), [])
        modules.preload(verbose=verbose)
        self.assertEqual(initial_path, self.get_env_path_list())

        modules.install("highs", verbose=verbose)
        self.assertNotEqual(initial_path, self.get_env_path_list())
        self.assertTrue(os.path.isfile(modules.find("highs")))

        modules.load("highs", verbose=verbose)
        self.assertNotEqual(initial_path, self.get_env_path_list())
        expected = modules.path().split(os.pathsep) + initial_path
        self.assertEqual(expected, self.get_env_path_list())
        self.assertEqual(len(initial_path) + 2, len(self.get_env_path_list()))
        self.assertIn(modules.path("highs", add_base=False), self.get_env_path_list())

        modules.install(["cbc"], verbose=verbose)
        modules.unload(["base", "cbc", "highs"])
        modules.load(["cbc", "highs"], verbose=verbose)
        expected = modules.path().split(os.pathsep) + initial_path
        self.assertEqual(expected, self.get_env_path_list())
        self.assertEqual(len(initial_path) + 3, len(self.get_env_path_list()))

        modules.unload("highs")
        self.assertNotEqual(initial_path, self.get_env_path_list())
        self.assertEqual(len(initial_path) + 2, len(self.get_env_path_list()))

        modules.unload(["cbc"])
        self.assertNotEqual(initial_path, self.get_env_path_list())
        self.assertEqual(len(initial_path) + 1, len(self.get_env_path_list()))

        modules.unload("base")
        self.assertEqual(initial_path, self.get_env_path_list())


if __name__ == "__main__":
    unittest.main()
