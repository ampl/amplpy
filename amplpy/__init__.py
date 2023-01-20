# -*- coding: utf-8 -*-
from __future__ import absolute_import


from .base import BaseClass
from .outputhandler import OutputHandler, Kind
from .errorhandler import ErrorHandler
from .exceptions import AMPLException
from .iterators import EntityMap
from .runnable import Runnable
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

try:
    from ampltools import register_magics
except Exception:
    pass
try:
    from ampltools import add_to_path
except Exception:
    pass

__version__ = "0.8.6b2"


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
                print("\t{} = {}".format(cammel_method, method))
                # setattr(cls, cammel_method, getattr(cls, method))
