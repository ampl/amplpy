#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

from .context import amplpy
import unittest
import tempfile
import shutil
import os


# For MSYS2, MINGW, etc., run with:
# $ REAL_ROOT=`cygpath -w /` python -m amplpy.tests
REAL_ROOT = os.environ.get('REAL_ROOT', None)


class TestBase(unittest.TestCase):
    def setUp(self):
        self.ampl = amplpy.AMPL()
        self.dirpath = tempfile.mkdtemp()

    def _tmpfile(self, filename):
        return os.path.join(self.dirpath, filename)

    def _real_filename(self, filename):
        # Workaround for MSYS2, MINGW paths
        if REAL_ROOT is not None and filename.startswith('/'):
            filename = filename.replace('/', REAL_ROOT, 1)
        return filename

    def str2file(self, filename, content):
        fullpath = self._tmpfile(filename)
        with open(fullpath, 'w') as f:
            print(content, file=f)
        return self._real_filename(fullpath)

    def tmpfile(self, filename):
        return self._real_filename(self._tmpfile(filename))

    def tearDown(self):
        self.ampl.close()
        shutil.rmtree(self.dirpath)


if __name__ == '__main__':
    unittest.main()
