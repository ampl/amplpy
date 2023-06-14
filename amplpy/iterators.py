# -*- coding: utf-8 -*-


class Iterator(object):
    def __init__(self, obj, function):
        self.obj = obj
        self.iterator = obj.begin()
        self.end = obj.end()
        self.function = function

    def __iter__(self):
        return self

    def __next__(self):
        if self.iterator.equals(self.end):
            raise StopIteration
        to_return = self.function(self.iterator)
        self.iterator.postIncrement()
        return to_return


class EntityMap(Iterator):
    def __init__(self, obj, entity_class):
        self.entity_class = entity_class

        def pair(iterator):
            entity = entity_class(iterator.__ref__())
            return (entity.name(), entity)

        Iterator.__init__(self, obj, pair)

    def __getitem__(self, key):
        assert isinstance(key, str)
        return self.entity_class(self.obj.getIndex(key))

    def size(self):
        return int(self.obj.size())

    def __len__(self):
        return self.size()


class InstanceIterator(Iterator):
    def __init__(self, obj, instanceClass):
        Iterator.__init__(
            self,
            obj,
            lambda it: (it.first(), instanceClass(it.second())),
        )

    def size(self):
        return int(self.obj.numInstances())

    def __len__(self):
        return self.size()


class MemberRangeIterator(Iterator):
    """Iterator for set members."""

    def __init__(self, obj):
        Iterator.__init__(self, obj, lambda it: it.__ref__())

    def size(self):
        return int(self.obj.size())

    def __len__(self):
        return self.size()


def EnvIterator(obj):
    """Iterator for environment classes."""
    return Iterator(obj, lambda it: (it.first(), it.second()))


def ColIterator(obj):
    return Iterator(obj, lambda it: it.__ref__())


def RowIterator(obj):
    return Iterator(obj, lambda it: it.__ref__())
