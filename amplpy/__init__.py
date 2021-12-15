# -*- coding: utf-8 -*-
from __future__ import absolute_import
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
from .dataframe import DataFrame
from .utils import multidict, register_magics
from .environment import Environment
from .ampl import AMPL
__version__ = '0.8.0b0'

import inflection
for cls in [
        OutputHandler, ErrorHandler,
        AMPLException, EntityMap, Runnable,
        Entity, Objective, Variable, Constraint, Set, Parameter,
        DataFrame, Environment, AMPL]:
    methods = list(dir(cls))
    for method in methods:
        snake_method = inflection.underscore(method)
        if snake_method != method and snake_method not in methods:
            # print(cls, snake_method, method)
            setattr(cls, snake_method, getattr(cls, method))
