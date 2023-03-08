#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import os

from .. import modules
from . import TestBase


class TestRun(TestBase.TestBase):
    """Test ampltools.modules: run, and activate."""

    def test_run_verbose(self):
        self._test_run(verbose=True)

    def test_run_silent(self):
        self._test_run(verbose=False)

    def _test_run(self, verbose):
        uuid = os.environ.get("AMPLKEY_UUID", None)
        if uuid is None:
            raise unittest.SkipTest("Needs AMPLKEY_UUID to run.")

        modules.install("base", verbose=verbose)
        modules.load("base", verbose=verbose)

        modules.activate(uuid, verbose=verbose)
        self.assertEqual(
            modules.run(f"amplkey activate --uuid {uuid}", verbose=verbose), 0
        )
        self.assertEqual(
            modules.run(["amplkey", "activate", "--uuid", uuid], verbose=verbose),
            0,
        )

    def test_error_verbose(self):
        self._test_error(verbose=True)

    def test_error_silent(self):
        self._test_error(verbose=False)

    def _test_error(self, verbose):
        modules.install("base", verbose=verbose)
        modules.load("base", verbose=verbose)

        with self.assertRaises(Exception) as context:
            modules.activate("invalid-uuid", verbose=verbose)
        self.assertTrue("The license activation failed." in str(context.exception))

        self.assertNotEqual(
            modules.run("amplkey activate --uuid invalid-uuid", verbose=verbose), 0
        )
        self.assertNotEqual(
            modules.run(
                ["amplkey", "activate", "--uuid", "invalid-uuid"], verbose=verbose
            ),
            0,
        )


if __name__ == "__main__":
    unittest.main()
