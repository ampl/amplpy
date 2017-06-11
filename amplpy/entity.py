from base import BaseClass
from utils import Tuple
from iterators import EntityIterator


class Entity(BaseClass):
    def __init__(self, _impl, wrapFunction=None):
        BaseClass.__init__(self, _impl)
        self.wrapFunction = wrapFunction

    def __iter__(self):
        assert self.wrapFunction is not None
        return EntityIterator(self._impl, self.wrapFunction)

    def __getitem__(self, *key):
        assert self.wrapFunction is not None
        if len(key) == 1 and isinstance(key, (tuple, list)):
            key = key[0]
        return self.wrapFunction(self.get(key))

    def get(self, index=None):
        assert self.wrapFunction is not None
        indexarity = self._impl.indexarity()
        if index is None:
            assert indexarity == 0
            return self.wrapFunction(self._impl.get())
        else:
            if not isinstance(index, (tuple, list)):
                index = (index,)
            assert indexarity == len(index)
            return self.wrapFunction(self._impl.get(Tuple(*index)._impl))
