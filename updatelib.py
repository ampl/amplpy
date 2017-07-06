#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import shutil
import tempfile


def updatelib():
    from zipfile import ZipFile
    try:
        from urllib import urlretrieve
    except Exception:
        from urllib.request import urlretrieve

    os.chdir(os.path.dirname(__file__) or os.curdir)

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
        if not os.path.isdir(dst):
            print('Downloading {}...'.format(url))
            name, hdrs = urlretrieve(url, tmpfile)
            with ZipFile(tmpfile) as zp:
                zp.extractall(dst)
    try:
        os.remove(tmpfile)
    except Exception:
        pass

    lib32 = os.path.join(tmpdir, 'lib32')
    lib64 = os.path.join(tmpdir, 'lib64')
    try:
        shutil.rmtree(lib32)
    except Exception:
        pass
    try:
        shutil.rmtree(lib64)
    except Exception:
        pass
    os.mkdir(lib32)
    os.mkdir(lib64)

    for libname, zipfile in builds:
        assert libname in ('lib32', 'lib64')
        for folder in ['lib', 'bin']:
            src = os.path.join(tmpdir, zipfile, 'amplapi', folder)
            if os.path.isdir(src):
                for filename in os.listdir(src):
                    if filename.endswith('.jar'):
                        continue
                    else:
                        shutil.copyfile(
                            os.path.join(src, filename),
                            os.path.join(tmpdir, libname, filename)
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

    for libname, lib in [('lib32', lib32), ('lib64', lib64)]:
        print('{}:'.format(libname))
        for filename in os.listdir(lib):
            print('\t{}'.format(filename))
            shutil.copyfile(
                os.path.join(lib, filename),
                os.path.join('amplpy', 'amplpython', libname, filename)
            )
            if filename.startswith('ampl-') and filename.endswith('.lib'):
                print('\t{}*'.format('ampl.lib'))
                shutil.copyfile(
                    os.path.join(lib, filename),
                    os.path.join('amplpy', 'amplpython', libname, 'ampl.lib')
                )


if __name__ == '__main__':
    updatelib()
