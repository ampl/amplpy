# -*- coding: utf-8 -*-
import sys
import os

from .base import BaseClass
from .outputhandler import OutputHandler, Kind
from .errorhandler import ErrorHandler
from .exceptions import AMPLException, PresolveException, InfeasibilityException
from .iterators import EntityMap
from .objective import Objective
from .variable import Variable
from .constraint import Constraint
from .set import Set
from .parameter import Parameter
from .entity import Entity
from .dataframe import DataFrame, Row, Column
from .utils import add_to_path, multidict, register_magics
from .environment import Environment
from .ampl import AMPL

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

__version__ = "0.13.3"


def _list_aliases():
    from inflection import camelize

    classes = [
        BaseClass,
        OutputHandler,
        ErrorHandler,
        AMPLException,
        EntityMap,
        Runnable,
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
