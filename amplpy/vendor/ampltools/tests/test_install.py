#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from .. import modules
from . import TestBase


class TestInstall(TestBase.TestBase):
    """Test ampltools.modules: install, uninstall, available, installed, and requirements."""

    def test_install_verbose(self):
        self._test_install(verbose=True)

    def test_install_silent(self):
        self._test_install(verbose=False)

    def _test_install(self, verbose):
        self.assertEqual(modules.installed(), [])

        modules.install("highs", verbose=verbose)
        self.assertEqual(modules.installed(), ["base", "highs"])

        with self.assertRaises(Exception) as context:
            modules.install("high", verbose=verbose)
        self.assertTrue(
            "AMPL module 'high' is not available." in str(context.exception)
        )

        with self.assertRaises(Exception) as context:
            modules.install("ipopt", verbose=verbose)
        self.assertTrue(
            "AMPL module 'ipopt' is not available. It is included in module 'coin'."
            in str(context.exception)
        )

        modules.install(["coin"], verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base", "highs", "coin"})

        modules.uninstall("highs", verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base", "coin"})

        with self.assertRaises(Exception) as context:
            modules.uninstall("base")

        self.assertTrue(
            "Base module cannot be uninstalled alone. You need to uninstall all modules."
            in str(context.exception)
        )

        modules.uninstall("coin", verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base"})

        modules.uninstall("base", verbose=verbose)
        self.assertEqual(modules.installed(), [])

        modules.install(["cbc", "highs"], verbose=verbose)
        self.assertEqual(set(modules.installed()), {"base", "highs", "cbc"})

        modules.uninstall(verbose=verbose)
        self.assertEqual(modules.installed(), [])

    def test_available(self):
        self.assertTrue(isinstance(modules.available(), list))
        self.assertGreaterEqual(len(modules.available()), 5)
        self.assertTrue("base" in modules.available())
        self.assertTrue("highs" in modules.available())
        self.assertTrue("coin" in modules.available())
        self.assertTrue("cbc" in modules.available())
        self.assertFalse("ipopt" in modules.available())

    def test_requirements(self):
        self.assertEqual(modules.installed(), [])
        ampl_pypi = "--index-url https://pypi.ampl.com"
        extra_pypi = "--extra-index-url https://pypi.org/simple"

        requirements = modules.requirements().strip().split("\n")
        print("requirements:", requirements)
        self.assertEqual(requirements[0], ampl_pypi)
        self.assertEqual(requirements[1], extra_pypi)
        self.assertEqual(len(requirements), 2)

        modules.install(["cbc", "highs"])

        requirements = modules.requirements().strip().split("\n")
        self.assertEqual(requirements[0], ampl_pypi)
        self.assertEqual(requirements[1], extra_pypi)
        self.assertTrue(
            any(req.startswith("ampl_module_base==") for req in requirements[2:])
        )
        self.assertTrue(
            any(req.startswith("ampl_module_cbc==") for req in requirements[2:])
        )
        self.assertTrue(
            any(req.startswith("ampl_module_highs==") for req in requirements[2:])
        )


if __name__ == "__main__":
    unittest.main()
