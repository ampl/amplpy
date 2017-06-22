from .entity import Entity
from .utils import Utils, Tuple
from .dataframe import DataFrame


class Parameter(Entity):
    """
    Represents an AMPL parameter. The values can be float or string (in case of
    symbolic parameters).

    Data can be assigned to the set using the methods
    :func:`~amplpy.Parameter.set` and :func:`~amplpy.Parameter.setValues` or
    using :func:`~amplpy.AMPL.setData` and an object of class
    :class:`~amplpy.DataFrame`.
    """

    def __init__(self, *args, **kwargs):
        _impl = kwargs.get('_impl', None)
        Entity.__init__(
            self,
            _impl,
            lambda it: Utils.castVariantRef(it)
        )

    def isSymbolic(self):
        """
        Returns True if the parameter is declared as symbolic (can store both
        numerical and string values).
        """
        return self._impl.isSymbolic()

    def hasDefault(self):
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

    def setValues(self, values):
        """
        Assign the values (string or float) to the parameter instances with the
        specified indices, equivalent to the AMPL code:

        .. code-block:: ampl

            let {i in indices} par[i] := values[i];

        Args:
            values: dictionary or :class:`~amplpy.DataFrame` with the indices
            and the values to be set.

        Raises:
            LogicError: If called on a scalar parameter.
        """
        if isinstance(values, dict):
            indices, values = zip(*values.items())
            indices = Utils.toTupleArray(indices)
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                self._impl.setValuesTaStr(indices, values, len(values))
            elif all(isinstance(value, (float, int)) for value in values):
                values = list(map(float, values))
                self._impl.setValuesTaDbl(indices, values, len(values))
            else:
                raise TypeError
        elif isinstance(values, (list, set)):
            if any(isinstance(value, basestring) for value in values):
                values = list(map(str, values))
                print(values)
                self._impl.setValuesStr(values, len(values))
            elif all(isinstance(value, (float, int)) for value in values):
                values = list(map(float, values))
                print(values)
                self._impl.setValuesDbl(values, len(values))
        elif isinstance(values, DataFrame):
            raise NotImplementedError
        else:
            raise TypeError

    def set(self, *args):
        """
        Set the value of a single instance of this parameter.

        Args:
            \*args: value if the parameter is scalar, index and value
            otherwise.

        Raises:
            RunTimeError: If the entity has been deleted in the underlying
            AMPL.

            LogicError: If the parameter is not scalar and the index is not
            provided.
        """
        assert len(args) in (1, 2)
        if len(args) == 1:
            value = args[0]
            self._impl.set(value)
        else:
            index, value = args
            self._impl.set(index, value)

    @classmethod
    def fromParameterRef(cls, prameterRef):
        return cls(_impl=prameterRef)
