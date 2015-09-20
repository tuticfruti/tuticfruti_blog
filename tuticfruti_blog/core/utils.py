from django.db.models.query import EmptyQuerySet


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


class MockQueryset(EmptyQuerySet):
    def __init__(self, model=None, items=list()):
        if model:
            self.model = model
        else:
            self.model = items[0].__class__
        self._result_cache = items

    def __len__(self):
        return len(self._result_cache)

    def __getitem__(self, key):
        return self._result_cache[key]

    def __setitem__(self, key, value):
        self._result_cache[key] = value
        return value

    def __delitem__(self, key):
        value = self._result_cache[key]
        del self._result_cache[key]
        return value

    def __iter__(self):
        return iter(self._result_cache)

    def __reversed__(self):
        return reversed(self._result_cache)

    def __contains__(self, item):
        return item in self._result_cache

    def __str__(self):
        return str(self._result_cache)

    def __repr__(self):
        return repr(self._result_cache)
