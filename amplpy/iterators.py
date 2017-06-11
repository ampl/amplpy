from utils import Utils, Tuple


class MapIterator:
    def __init__(self, function, entity):
        self.entity = entity
        self.it = entity.begin()
        self.end = entity.end()
        self.function = function

    def __iter__(self):
        return self

    def next(self):
        if self.it.equals(self.end):
            raise StopIteration
        toReturn = self.function(self.it)
        self.it.postIncrement()
        return toReturn


def EntityIterator(entity, entityClass):
    return MapIterator(
        lambda it: (
            Tuple.fromTupleRef(it.first()).toPyObj(),
            entityClass(it.second())
        ),
        entity
    )


def MemberRangeIterator(entity):
    """Iterator for set members."""
    return MapIterator(
        lambda it: Tuple.fromTupleRef(it.__ref__()).toPyObj(),
        entity
    )


def EnvIterator(entity):
    """Iterator for environment classes."""
    return MapIterator(
        lambda it: (it.first(), it.second()),
        entity
    )


def MapEntities(function, entity):
    return MapIterator(
        lambda it: function(it.__ref__()),
        entity
    )


def ColIterator(entity):
    return MapIterator(
        lambda it: Utils.castVariantRef(it.__ref__()),
        entity
    )


def RowIterator(entity):
    return MapIterator(
        lambda it: Utils.castVariantRef(it.__ref__()),
        entity
    )
