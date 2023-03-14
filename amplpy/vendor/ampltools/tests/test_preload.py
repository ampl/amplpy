#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from .. import modules
from . import TestBase


class TestPreload(TestBase.TestBase):
    """Test ampltools.modules: preload."""

    def test_preload_verbose(self):
        self._test_preload(verbose=True)

    def test_preload_silent(self):
        self._test_preload(verbose=False)

    def _test_preload(self, verbose):
        """When preloading without ampl_module_base it is not loaded
        afterwards unless we reload modules.
        """
        modules.unload()
        initial_path = self.get_env_path_list()
        modules.preload(verbose=verbose)
        self.assertEqual(modules.installed(), [])
        requirements = modules.requirements().strip().split("\n")
        self.assertEqual(len(requirements), 2)

        with self.assertRaises(Exception) as context:
            modules.load("cbc", verbose=verbose)
        self.assertTrue(
            "Module ampl_module_base needs to be reinstalled." in str(context.exception)
        )

        modules.install(["cbc"], verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base", "cbc"})
        modules.load()
        self.assertTrue(
            any("ampl_module_cbc" in path for path in self.get_env_path_list())
        )
        self.assertTrue(
            any("ampl_module_base" in path for path in self.get_env_path_list())
        )

        self.assertEqual(len(initial_path) + 2, len(self.get_env_path_list()))

        requirements = modules.requirements().strip().split("\n")
        self.assertEqual(len(requirements), 4)

        self.assertTrue(
            any(req.startswith("ampl_module_base==") for req in requirements[2:])
        )
        self.assertTrue(
            any(req.startswith("ampl_module_cbc==") for req in requirements[2:])
        )

        modules.uninstall(["cbc"], verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base"})

        self.assertEqual(len(initial_path) + 1, len(self.get_env_path_list()))

        requirements = modules.requirements().strip().split("\n")
        self.assertEqual(len(requirements), 3)

        self.assertTrue(
            any(req.startswith("ampl_module_base==") for req in requirements[2:])
        )
        self.assertFalse(
            any(req.startswith("ampl_module_cbc==") for req in requirements[2:])
        )


if __name__ == "__main__":
    unittest.main()
