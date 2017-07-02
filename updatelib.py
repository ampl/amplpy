#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from zipfile import ZipFile
import os
import shutil
import urllib
import tempfile


builds = [
    ('lib32', 'amplapi-linux32.zip'),
    ('lib32', 'amplapi-win32.zip'),
    ('lib64', 'amplapi-linux64.zip'),
    ('lib64', 'amplapi-win64.zip'),
    ('lib64', 'amplapi-osx.zip')
]

tmpdir = os.path.join(os.curdir, 'tmp')
tmpfile = tempfile.mktemp('.zip')
for lib, zipfile in builds:
    url = 'http://ampl.com/dl/API/latest/{}'.format(zipfile)
    dst = os.path.join(tmpdir, zipfile)
    if os.path.isdir(dst) is False:
        name, hdrs = urllib.urlretrieve(url, tmpfile)
        with ZipFile(tmpfile) as zp:
            zp.extractall(dst)
try:
    os.remove(tmpfile)
except Exception:
    pass

lib32 = os.path.join(tmpdir, 'lib32')
lib64 = os.path.join(tmpdir, 'lib64')
shutil.rmtree(lib32)
shutil.rmtree(lib64)
os.mkdir(lib32)
os.mkdir(lib64)

for lib, zipfile in builds:
    assert lib in ('lib32', 'lib64')
    src = os.path.join(tmpdir, zipfile, 'amplapi', 'lib')
    for filename in os.listdir(src):
        if filename.endswith('.jar'):
            continue
        else:
            shutil.copyfile(
                os.path.join(src, filename),
                os.path.join(tmpdir, lib, filename)
            )

include_dir = os.path.join(
    tmpdir, 'amplapi-linux64.zip', 'amplapi', 'include', 'ampl'
)
amplpy_include = os.path.join('amplpy', 'amplpython', 'include', 'ampl')
try:
    shutil.rmtree(amplpy_include)
except Exception:
    pass
shutil.copytree(include_dir, amplpy_include)

print('lib32:')
for filename in os.listdir(lib32):
    print('\t{}'.format(filename))
    shutil.copyfile(
        os.path.join(lib32, filename),
        os.path.join('amplpy', 'amplpython', 'lib32', filename)
    )


print('lib64:')
for filename in os.listdir(lib64):
    print('\t{}'.format(filename))
    shutil.copyfile(
        os.path.join(lib64, filename),
        os.path.join('amplpy', 'amplpython', 'lib64', filename)
    )
