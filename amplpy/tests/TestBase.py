#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division
from builtins import map, range, object, zip, sorted

from .context import amplpy
import unittest
import tempfile
import shutil
import os


class TestBase(unittest.TestCase):
    def setUp(self):
        self.ampl = amplpy.AMPL()
        self.dirpath = tempfile.mkdtemp()

    def str2file(self, filename, content):
        fullpath = self.tmpfile(filename)
        with open(fullpath, 'w') as f:
            print(content, file=f)
        return fullpath

    def tmpfile(self, filename):
        return os.path.join(self.dirpath, filename)

    def tearDown(self):
        self.ampl.close()
        shutil.rmtree(self.dirpath)


if __name__ == '__main__':
    unittest.main()
