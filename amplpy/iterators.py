from .utils import Utils, Tuple


class Iterator:
    def __init__(self, function, entity):
        self.entity = entity
        self.it = entity.begin()
        self.end = entity.end()
        self.function = function

    def __iter__(self):
        return self

    def __getitem__(self, key):
        assert isinstance(key, basestring)
        return self.function(self.entity.getIndex(key))

    def next(self):
        if self.it.equals(self.end):
            raise StopIteration
        toReturn = self.function(self.it)
        self.it.postIncrement()
        return toReturn

    def size(self):
        return int(self.entity.size())

    def __len__(self):
        return self.size()


def EntityIterator(entity, entityClass):
    return Iterator(
        lambda it: (
            Tuple.fromTupleRef(it.first()).toPyObj(),
            entityClass(it.second())
        ),
        entity
    )


def MemberRangeIterator(entity):
    """Iterator for set members."""
    return Iterator(
        lambda it: Tuple.fromTupleRef(it.__ref__()).toPyObj(),
        entity
    )


def EnvIterator(entity):
    """Iterator for environment classes."""
    return Iterator(
        lambda it: (it.first(), it.second()),
        entity
    )


def MapEntities(function, entity):
    return Iterator(
        lambda it: function(it.__ref__()),
        entity
    )


def ColIterator(entity):
    return Iterator(
        lambda it: Utils.castVariantRef(it.__ref__()),
        entity
    )


def RowIterator(entity):
    return Iterator(
        lambda it: Utils.castVariantRef(it.__ref__()),
        entity
    )
