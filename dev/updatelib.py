#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import tempfile

VERSION = "nightly/v3"
API_URL = f"https://portal.ampl.com/~jurgen/jl/libampl.zip"
ARCHS = ["amd64", "ppc64le", "aarch64"]


def updatelib(package, archs):
    from zipfile import ZipFile

    try:
        from urllib import urlretrieve
    except Exception:
        from urllib.request import urlretrieve

    os.chdir(os.path.join(os.path.dirname(__file__), "..") or os.curdir)

    tmpfile = tempfile.mktemp(".zip")
    tmpdir = os.path.join(os.curdir, "tmp")
    libampldir = os.path.join(tmpdir, "libampl")
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

    if package.startswith("http"):
        # Disable SSL verification
        import ssl

        ssl._create_default_https_context = ssl._create_unverified_context
        print("Downloading:", API_URL)
        urlretrieve(API_URL, tmpfile)
        with ZipFile(tmpfile) as zp:
            zp.extractall(tmpdir)
        try:
            os.remove(tmpfile)
        except Exception:
            pass
    else:
        with ZipFile(package) as zp:
            zp.extractall(tmpdir)

    include_dir = os.path.join(libampldir, "include", "ampl")
    wrapper_dir = os.path.join(libampldir, "python")

    amplpy_include = os.path.join(
        "amplpy", "amplpython", "cppinterface", "include", "ampl"
    )
    try:
        shutil.rmtree(amplpy_include)
    except Exception:
        pass
    shutil.copytree(include_dir, amplpy_include)
    print(
        "*\n!.gitignore\n", file=open(os.path.join(amplpy_include, ".gitignore"), "w")
    )

    # print('wrapper:')
    # for filename in os.listdir(wrapper_dir):
    #     print(f'\t{filename}')
    #     shutil.copyfile(
    #         os.path.join(wrapper_dir, filename),
    #         os.path.join('amplpy', 'amplpython', 'cppinterface', filename)
    #     )

    dstbase = os.path.join("amplpy", "amplpython", "cppinterface", "lib")
    try:
        shutil.rmtree(dstbase)
        os.mkdir(dstbase)
    except Exception:
        pass
    print("*\n!.gitignore\n", file=open(os.path.join(dstbase, ".gitignore"), "w"))

    for libname in archs:
        srcdir = os.path.join(libampldir, libname)
        dstdir = os.path.join(dstbase, libname)
        os.mkdir(dstdir)
        print(f"{libname}:")
        for filename in os.listdir(srcdir):
            print(f"\t{filename}")
            shutil.copyfile(
                os.path.join(srcdir, filename), os.path.join(dstdir, filename)
            )


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     updatelib(API_URL, sys.argv[1:])
    # else:
    #     updatelib(API_URL, ['intel32', 'amd64', 'ppc64le', 'aarch64'])
    if len(sys.argv) == 2:
        updatelib(sys.argv[1], ARCHS)
    else:
        updatelib(API_URL, ARCHS)
