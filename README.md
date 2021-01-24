# AMPLPY

[![PyPI - Downloads](https://img.shields.io/pypi/dm/amplpy?label=PyPI%20downloads)](https://pypistats.org/packages/amplpy)
[![Conda](https://img.shields.io/conda/dn/conda-forge/amplpy?label=Conda%20downloads)](https://anaconda.org/conda-forge/amplpy)
[![Build Status](https://dev.azure.com/ampldev/amplpy/_apis/build/status/ampl.amplpy?branchName=test)](https://dev.azure.com/ampldev/amplpy/_build/latest?definitionId=9&branchName=test)


AMPL API is an interface that allows developers to access the features of the
AMPL interpreter from within a programming language. All model generation and
solver interaction is handled directly by AMPL, which leads to great stability
and speed; the library just acts as an intermediary, and the added overhead
(in terms of memory and CPU usage) depends mostly on how much data is read
back from AMPL, the size of the model as such is irrelevant. Functions for
directly assigning data to AMPL parameters and sets are provided, which can
be used instead of the normal AMPL data reading procedures.  AMPL API has been
written with usability in mind, and it is easy to access its functionalities
from C++, Java, C#, MATLAB, R and Python.

The AMPL API can function as an add-on to any existing AMPL installation. If
you do not yet have an AMPL installation on the computer where you will be
working with the API, see our
[demo page](http://ampl.com/try-ampl/download-a-free-demo/)
or
[trial page](http://ampl.com/try-ampl/request-a-full-trial/)
to download a working version that can be installed quickly.

## Documentation

- http://amplpy.readthedocs.io
- http://ampl.com/api/nightly/python/

## Examples

- Quick start: [Introductory Tutorial](notebooks/quickstart.ipynb)

- More examples:
  - [examples/](examples/)
  - [notebooks/](notebooks/)

## Repositories

- GitHub Repository: https://github.com/ampl/amplpy
- PyPI Repository: https://pypi.python.org/pypi/amplpy
- Conda-Forge: https://anaconda.org/conda-forge/amplpy

## Setup

### PyPI

Install from the [PyPI repository](https://pypi.python.org/pypi/amplpy):
```
$ pip install amplpy
```
Or:
```
$ python -m pip install amplpy
```

Note: For Windows, Linux, and macOS, the `amplpy` package comes with binary wheels for Python 2.7, 3.5, 3.6, 3.7, 3.8, and 3.9. Please make sure that you are using the latest version of `pip` before installing `amplpy` (upgrade using `pip install pip --upgrade` or `python -m pip install pip --upgrade`). If a binary wheel for your platform is not available, a C++ compiler and python development libraries will be required.

### Conda

Install from the [Conda repository](https://anaconda.org/conda-forge/amplpy):
```
$ conda install -c conda-forge amplpy
```

### Build locally

You can build and install the package locally as follows:
```
$ git clone git@github.com:ampl/amplpy.git
$ cd amplpy
$ python updatelib.py
$ python setup.py build
$ pip install . --upgrade
```

## License

BSD-3

***
Copyright © 2017-2021 AMPL Optimization inc. All rights reserved.
