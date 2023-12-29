#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import tempfile
import shutil
import os
from .context import amplpy


# For MSYS2, MINGW, etc., run with:
# $ REAL_ROOT=`cygpath -w /` python -m amplpy.tests
REAL_ROOT = os.environ.get("REAL_ROOT", None)


class TestBase(unittest.TestCase):
    def setUp(self):
        print("setUp:", self._testMethodName)
        self.ampl = amplpy.AMPL()
        self.ampl.option["solver"] = "highs"
        self.ampl.option["highs_options"] = "outlev=1"
        self.dirpath = tempfile.mkdtemp()

    def _tmpfile(self, filename):
        return os.path.join(self.dirpath, filename)

    def _real_filename(self, filename):
        # Workaround for MSYS2, MINGW paths
        if REAL_ROOT is not None and filename.startswith("/"):
            filename = filename.replace("/", REAL_ROOT, 1)
        return filename

    def str2file(self, filename, content):
        fullpath = self._tmpfile(filename)
        with open(fullpath, "w") as file:
            print(content, file=file)
        return self._real_filename(fullpath)

    def tmpfile(self, filename):
        return self._real_filename(self._tmpfile(filename))

    def tearDown(self):
        print("tearDown:", self._testMethodName)
        self.ampl.close()
        shutil.rmtree(self.dirpath)
        print("done!")


if __name__ == "__main__":
    unittest.main()
