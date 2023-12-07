# AMPLPY: Python API for AMPL

[![PyPI - Downloads](https://img.shields.io/pypi/dm/amplpy?label=PyPI%20downloads)](https://pypistats.org/packages/amplpy)
[![Conda](https://img.shields.io/conda/dn/conda-forge/amplpy?label=Conda%20downloads)](https://anaconda.org/conda-forge/amplpy)
[![Build Status](https://dev.azure.com/ampldev/amplpy/_apis/build/status/ampl.amplpy?branchName=master)](https://dev.azure.com/ampldev/amplpy/_build/latest?definitionId=9&branchName=test)
[![build-and-test](https://github.com/ampl/amplpy/actions/workflows/build-and-test.yaml/badge.svg)](https://github.com/ampl/amplpy/actions/workflows/build-and-test.yaml)

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

[![Hands-On Mathematical Optimization with AMPL in Python](https://portal.ampl.com/dl/ads/mo_book_big.png)](https://ampl.com/mo-book/)

[[Documentation](https://amplpy.readthedocs.io/)] [[AMPL Modules for Python](https://dev.ampl.com/ampl/python/modules.html)] [[AMPL on Streamlit](https://ampl.com/streamlit)] [[AMPL on Google Colab](https://colab.ampl.com/)] [[Community Edition](https://ampl.com/ce)]

`amplpy` is an interface that allows developers to access the features of [AMPL](https://ampl.com) from within Python. For a quick introduction to AMPL see [Quick Introduction to AMPL](https://dev.ampl.com/ampl/introduction.html).

In the same way that AMPL’s syntax matches naturally the mathematical description of the model, the input and output data matches naturally Python lists, sets, dictionaries, `pandas` and `numpy` objects.

All model generation and solver interaction is handled directly by AMPL, which leads to great stability and speed; the library just acts as an intermediary, and the added overhead (in terms of memory and CPU usage) depends mostly on how much data is sent and read back from AMPL, the size of the expanded model as such is irrelevant.

With `amplpy` you can model and solve large scale optimization problems in Python with the performance of heavily optimized C code without losing model readability. The same model can be deployed on applications built on different languages by just switching the API used.

## Documentation

- http://amplpy.readthedocs.io

## Examples

Data can be loaded in various forms:
- One of which is ``pandas.DataFrame`` objects:

    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/pandasdiet.ipynb)
- Python lists and dictionaries:
     
     [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ampl/amplcolab/blob/master/authors/fdabrandao/quick-start/nativediet.ipynb)

More notebooks with examples available on the [AMPL Model Colaboratory](https://colab.ampl.com/).

## Repositories

- GitHub Repository: https://github.com/ampl/amplpy
- PyPI Repository: https://pypi.python.org/pypi/amplpy
- Conda-Forge: https://anaconda.org/conda-forge/amplpy

## Setup

### PyPI

Install from the [PyPI repository](https://pypi.python.org/pypi/amplpy):

```
python -m pip install amplpy
```

### AMPL Modules for Python

[AMPL and all Solvers are now available as Python Packages](https://dev.ampl.com/ampl/python/modules.html):

- Install Python API for AMPL:
    ```
    python -m pip install amplpy --upgrade
    ```

- Install solver modules (e.g., HiGHS and Gurobi):
    ```
    python -m amplpy.modules install highs gurobi
    ```

- Activate your license (e.g., free [AMPL Community Edition](https://ampl.com/ce) license):
    ```
    python -m amplpy.modules activate <license-uuid>
    ```

- Import and instantiate in Python:
    ```
    $ python
    >>> from amplpy import AMPL
    >>> ampl = AMPL() # instantiate AMPL object
    ```

### Conda

Install from the [Conda repository](https://anaconda.org/conda-forge/amplpy):

```
conda install -c conda-forge amplpy
```

### Air-gapped installation

For air-gapped installations we recomend the following:
- Download on another machine the `.whl` file for the corresponding platform and python version from [pypi](https://pypi.org/project/amplpy/#files).
- Install on the target machine with: `python -m pip install amplpy-version-python_version-*-platform.whl --no-deps`

### Build locally

You can build and install the package locally as follows:
```
$ git clone https://github.com/ampl/amplpy.git 
$ cd amplpy
$ python dev/updatelib.py
$ python setup.py build
$ pip install . --upgrade
```

## License

BSD-3

***
Copyright © 2023 AMPL Optimization inc. All rights reserved.
