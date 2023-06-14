# -*- coding: utf-8 -*-


class BaseClass(object):
    def __init__(self, _impl):
        self._impl = _impl

    def to_string(self):
        return self._impl.toString()

    def __str__(self):
        return self.to_string()

    # Aliases
    toString = to_string
