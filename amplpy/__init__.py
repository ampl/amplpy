# -*- coding: utf-8 -*-
import sys
import os
import platform
import ctypes


if platform.system().startswith(("Windows", "MSYS", "CYGWIN", "MINGW")):
    libbase = os.path.join(os.path.dirname(__file__), "amplpython", "cppinterface", "lib")
    lib64 = os.path.join(libbase, "amd64")
    from glob import glob

    try:
        dllfile = glob(lib64 + "/*.dll")[0]
        ctypes.CDLL(dllfile)
    except Exception as exp:
        raise exp

from _amplpy import OutputHandler, Kind
from _amplpy import ErrorHandler
from _amplpy import AMPLException, PresolveException, InfeasibilityException
from _amplpy import EntityMap
from _amplpy import Objective
from _amplpy import Variable
from _amplpy import Constraint
from _amplpy import Set
from _amplpy import Parameter
from _amplpy import Entity
from _amplpy import DataFrame, Row, Column
from .utils import add_to_path, multidict, register_magics
from _amplpy import Environment
from _amplpy import AMPL

_parent_dir = os.path.abspath(os.path.dirname(__file__))
_vendor_dir = os.path.join(_parent_dir, "vendor")
if _vendor_dir not in sys.path:
    sys.path.append(_vendor_dir)

try:
    from ampltools import register_magics
except Exception:
    pass
try:
    from ampltools import ampl_notebook
except Exception:
    pass
try:
    from ampltools import add_to_path
except Exception:
    pass
try:
    from . import modules

    modules.preload()
except Exception:
    pass

__version__ = "0.15.0b0"


def _list_aliases():
    from inflection import camelize

    classes = [
        OutputHandler,
        ErrorHandler,
        AMPLException,
        EntityMap,
        Entity,
        Objective,
        Variable,
        Constraint,
        Set,
        Parameter,
        Row,
        Column,
        DataFrame,
        Environment,
        AMPL,
    ]
    for cls in classes:
        print(cls)
        for method in list(dir(cls)):
            if method.startswith("__"):
                continue
            cammel_method = camelize(method, False)
            if cammel_method != method:
                print(f"\t{cammel_method} = {method}")
                # setattr(cls, cammel_method, getattr(cls, method))
