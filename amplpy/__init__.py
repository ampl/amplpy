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

from amplpy.ampl import OutputHandler, Kind
from amplpy.ampl import ErrorHandler
from amplpy.ampl import AMPLException, PresolveException, InfeasibilityException
from amplpy.ampl import EntityMap
from amplpy.ampl import Objective
from amplpy.ampl import Variable
from amplpy.ampl import Constraint
from amplpy.ampl import Set
from amplpy.ampl import Parameter
from amplpy.ampl import Entity
from amplpy.ampl import DataFrame, Row, Column
from .utils import add_to_path, multidict, register_magics
from amplpy.ampl import Environment
from amplpy.ampl import AMPL
from amplpy.ampl import logger

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

__version__ = "0.15.2"


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
