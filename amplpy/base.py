class BaseClass(object):
    def __init__(self, _impl):
        self._impl = _impl

    def toString(self):
        return self._impl.toString()

    def __str__(self):
        return self.toString()
