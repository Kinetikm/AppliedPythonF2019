import time
from functools import wraps
from collections import OrderedDict


def make_key(args, kwds):
    kwd_mark = (object(),)
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item

    return key


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
         :param ttl: время в млсек, через которое кеш
                     должен исчезнуть
                     МАксимально возможно  для своих знаний оптимизировал декоратор
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()
        self.times = {}

    def __call__(self, func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            key = make_key(args, kwargs)
            value = self.cache.get(key, None)
            if value is not None and self.ttl is not None and (time.time() - self.times[key]) > self.ttl:
                self.cache.pop(key)
                value = None

            if value is None:
                value = func(*args, **kwargs)
                if len(self.cache) == self.maxsize:
                    self.cache.popitem()
                self.cache[key] = value

            self.times[key] = time.time()

            return value

        return wrapped
