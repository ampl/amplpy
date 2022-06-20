# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, division

# from builtins import map, range, object, zip, sorted
from builtins import map
from numbers import Real
from past.builtins import basestring

from .entity import Entity
from .dataframe import DataFrame

try:
    import numpy as np
except ImportError:
    np = None


class Parameter(Entity):
    """
    Represents an AMPL parameter. The values can be float or string (in case of
    symbolic parameters).

    Data can be assigned to the set using the methods
    :func:`~amplpy.Parameter.set` and
    :func:`~amplpy.Parameter.set_values` / :func:`~amplpy.Parameter.setValues`
    or using
    :func:`~amplpy.AMPL.set_data` / :func:`~amplpy.AMPL.setData`
    and an object of class :class:`~amplpy.DataFrame`.
    """

    def __init__(self, _impl):
        Entity.__init__(self, _impl, lambda it: it)

    def __setitem__(self, index, value):
        self.set(index, value)

    def is_symbolic(self):
        """
        Returns True if the parameter is declared as symbolic (can store both
        numerical and string values).
        """
        return self._impl.isSymbolic()

    def has_default(self):
        """
        Check if the parameter has a default initial value. In case of the
        following AMPL code:

        .. code-block:: ampl

            param a;
            param b default a;

        the function will return true for parameter ``b``.

        Returns:
            True if the parameter has a default initial value. Please note
            that if the parameter has a default expression which refers to
            another parameter which value is not defined, this will return
            True.
        """
        return self._impl.hasDefault()

    def value(self):
        """
        Get the value of this parameter. Valid only for non-indexed parameters.
        """
        return self.get()

    def set(self, *args):
        """
        Set the value of a single instance of this parameter.

        Args:
            args: value if the parameter is scalar, index and value
            otherwise.

        Raises:
            RuntimeError: If the entity has been deleted in the underlying
            AMPL.

            TypeError: If the parameter is not scalar and the index is not
            provided.
        """
        assert len(args) in (1, 2)
        if len(args) == 1:
            value = args[0]
            self._impl.set(value)
        else:
            index, value = args
            if isinstance(value, Real):
                self._impl.setTplDbl(index, value)
            elif isinstance(value, basestring):
                self._impl.setTplStr(index, value)
            else:
                raise TypeError

    def set_values(self, values):
        """
        Assign the values (string or float) to the parameter instances with the
        specified indices, equivalent to the AMPL code:

        .. code-block:: ampl

            let {i in indices} par[i] := values[i];

        Args:
            values: list, dictionary or :class:`~amplpy.DataFrame` with the
            indices and the values to be set.

        Raises:
            TypeError: If called on a scalar parameter.
        """
        if isinstance(values, dict):
            if not values:
                return
            self._impl.setValuesPyDict(values)
        elif isinstance(values, (list, tuple)):
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                self._impl.setValuesStr(values, len(values))
            elif all(isinstance(value, Real) for value in values):
                values = list(map(float, values))
                self._impl.setValuesDbl(values, len(values))
            else:
                raise TypeError
        else:
            if np is not None and isinstance(values, np.ndarray):
                self.set_values(DataFrame.from_numpy(values).to_list())
                return
            Entity.set_values(self, values)

    # Aliases
    hasDefault = has_default
    isSymbolic = is_symbolic
    setValues = set_values
