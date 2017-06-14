from .entity import Entity
from .utils import Utils
from .iterators import MemberRangeIterator


class Set(Entity):
    def __init__(self, *args, **kwargs):
        _impl = kwargs.get('_impl', None)
        Entity.__init__(
            self,
            _impl,
            lambda it: MemberRangeIterator(it.members())
        )

    def getValues(self):
        raise NotImplementedError

    @classmethod
    def fromSetRef(cls, setRef):
        return cls(_impl=setRef)


class Parameter(Entity):
    def __init__(self, *args, **kwargs):
        _impl = kwargs.get('_impl', None)
        Entity.__init__(
            self,
            _impl,
            lambda it: Utils.castVariantRef(it)
        )

    @classmethod
    def fromParameterRef(cls, prameterRef):
        return cls(_impl=prameterRef)
