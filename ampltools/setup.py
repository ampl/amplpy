# -*- coding: utf-8 -*-
"""
AMPL Python Tools
-----------------

This package includes tools to use with AMPL and amplpy.

Links
`````

* GitHub Repository: https://github.com/ampl/amplpy/tree/master/ampltools
* PyPI Repository: https://pypi.python.org/pypi/ampltools
"""
from setuptools import setup
import os


def ls_dir(base_dir):
    """List files recursively."""
    return [
        os.path.join(dirpath.replace(base_dir, "", 1), f)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for f in files
    ]


setup(
    name="ampltools",
    version="0.4.4",
    description="AMPL Python Tools",
    long_description=__doc__,
    license="BSD-3",
    platforms="any",
    author="Filipe Brandão",
    author_email="fdabrandao@ampl.com",
    url="http://ampl.com/",
    download_url="https://github.com/ampl/amplpy/tree/master/ampltools",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=open("requirements.txt").read().split("\n"),
    packages=["ampltools"],
    package_data={"": ls_dir("ampltools/")},
)
