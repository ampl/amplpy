# -*- coding: utf-8 -*-
'''
# AMPLPY: Python API for AMPL

```python
# Install Python API for AMPL
$ python -m pip install amplpy --upgrade

# Install solver modules (e.g., HiGHS, CBC, Gurobi)
$ python -m amplpy.modules install highs cbc gurobi

# Activate your license (e.g., free https://ampl.com/ce license)
$ python -m amplpy.modules activate <license-uuid>

# Import in Python
$ python
>>> from amplpy import AMPL
>>> ampl = AMPL() # instantiate AMPL object
```

```python
# Minimal example:
from amplpy import AMPL
import pandas as pd
ampl = AMPL()
ampl.eval(r"""
    set A ordered;
    param S{A, A};
    param lb default 0;
    param ub default 1;
    var w{A} >= lb <= ub;
    minimize portfolio_variance:
        sum {i in A, j in A} w[i] * S[i, j] * w[j];
    s.t. portfolio_weights:
        sum {i in A} w[i] = 1;
""")
tickers, cov_matrix = # ... pre-process data in Python
ampl.set["A"] = tickers
ampl.param["S"] = pd.DataFrame(cov_matrix, index=tickers, columns=tickers)
ampl.option["solver"] = "gurobi"
ampl.option["gurobi_options"] = "outlev=1"
ampl.solve()
assert ampl.solve_result == "solved"
sigma = ampl.get_value("sqrt(sum {i in A, j in A} w[i] * S[i, j] * w[j])")
print(f"Volatility: {sigma*100:.1f}%")
# ... post-process solution in Python
```

[[Documentation](https://amplpy.readthedocs.io/)] [[AMPL Modules for Python](https://dev.ampl.com/ampl/python/modules.html)] [[Available on Google Colab](https://colab.ampl.com/)] [[AMPL Community Edition](http://ampl.com/ce)]

`amplpy` is an interface that allows developers to access the features of [AMPL](https://ampl.com) from within Python. For a quick introduction to AMPL see [Quick Introduction to AMPL](https://dev.ampl.com/ampl/introduction.html).

In the same way that AMPL’s syntax matches naturally the mathematical description of the model, the input and output data matches naturally Python lists, sets, dictionaries, `pandas` and `numpy` objects.

All model generation and solver interaction is handled directly by AMPL, which leads to great stability and speed; the library just acts as an intermediary, and the added overhead (in terms of memory and CPU usage) depends mostly on how much data is sent and read back from AMPL, the size of the expanded model as such is irrelevant.

With `amplpy` you can model and solve large scale optimization problems in Python with the performance of heavily optimized C code without losing model readability. The same model can be deployed on applications built on different languages by just switching the API used.

## Documentation

- http://amplpy.readthedocs.io

## Repositories:

* GitHub Repository: https://github.com/ampl/amplpy
* PyPI Repository: https://pypi.python.org/pypi/amplpy
'''
from setuptools import setup, Extension
import platform
import sys
import os

OSTYPE = platform.system()
ARCH = platform.processor() or platform.machine()
x64 = platform.architecture()[0] == "64bit"

if ARCH == "ppc64le":
    LIBRARY = "ppc64le"
elif ARCH == "aarch64":
    LIBRARY = "aarch64"
else:  # 'AMD64', 'x86_64', 'i686', 'i386'
    LIBRARY = "amd64" if x64 else "intel32"

if OSTYPE == "Darwin":
    LIBRARY_EXT = ".dylib"
elif OSTYPE == "Linux":
    LIBRARY_EXT = ".so"
else:
    LIBRARY_EXT = ".dll"

CPP_BASE = os.path.join("amplpy", "amplpython", "cppinterface")
LIBRARY_BASE = os.path.join(CPP_BASE, "lib")
LIBRARY_DIR = os.path.join(LIBRARY_BASE, LIBRARY)


def ls_dir(base_dir):
    """List files recursively."""
    return [
        os.path.join(dirpath, fname)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for fname in files
    ]


def package_content():
    all_files = ls_dir("amplpy/")
    if "sdist" in sys.argv:
        lst = all_files
    else:
        source_only = [
            fpath for fpath in all_files if not fpath.startswith(LIBRARY_BASE)
        ]
        library_only = [
            fpath
            for fpath in all_files
            if fpath.startswith(LIBRARY_DIR)
            if fpath.endswith(LIBRARY_EXT)
        ]
        lst = source_only + library_only
    return [fpath.replace("amplpy/", "", 1) for fpath in lst]


def compile_args():
    if OSTYPE == "Windows":
        return ["/TP", "/EHa"]
    elif OSTYPE == "Linux":
        ignore_warnings = [
            "-Wno-stringop-truncation",
            "-Wno-catch-value",
            "-Wno-unused-variable",
        ]
        return ["-std=c++11"] + ignore_warnings
    elif OSTYPE == "Darwin":
        ignore_warnings = [
            "-Wno-unused-variable",
        ]
        debug = []
        if os.environ.get("DEBUG", None) == "1":
            debug = [
                "-g",
                "-fno-omit-frame-pointer",
            ]
        return (
            [
                "-std=c++11",
                "-mmacosx-version-min=10.9",
            ]
            + debug
            + ignore_warnings
        )
    else:
        return []


def link_args():
    rpath = os.path.join(LIBRARY_BASE, LIBRARY)
    if OSTYPE == "Darwin":
        return ["-Wl,-rpath,@loader_path/" + rpath]
    elif OSTYPE == "Linux":
        return ["-Wl,-rpath,$ORIGIN/" + rpath]
    else:
        # Return [] instead of [''] for Windows in order to avoid:
        #  cannot open input file '.obj' in build on distutils from Python 3.9
        # https://github.com/pypa/setuptools/issues/2417
        return []


setup(
    name="amplpy",
    version="0.12.2",
    description="Python API for AMPL",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    license="BSD-3",
    platforms="any",
    author="AMPL Optimization Inc.",
    author_email="devteam@ampl.com",
    url="http://ampl.com/",
    download_url="https://github.com/ampl/amplpy",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
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
        "Programming Language :: C++",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    packages=["amplpy"],
    ext_modules=[
        Extension(
            "_amplpython",
            libraries=["ampl"],
            library_dirs=[os.path.join(LIBRARY_BASE, LIBRARY)],
            include_dirs=[os.path.join(CPP_BASE, "include")],
            extra_compile_args=compile_args(),
            extra_link_args=link_args(),
            sources=[os.path.join(CPP_BASE, "amplpythonPYTHON_wrap.cxx")],
        )
    ],
    package_data={"": package_content()},
    install_requires=["ampltools >= 0.6.2"],
)
