from time import time
from collections import OrderedDict
import functools


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, str(kwargs), str(kwargs.values()))
            if key in self.cache:
                if self.ttl:
                    if (time() - self.cache[key][1]) * 1000 > self.ttl:
                        res = func(*args, **kwargs)
                        self.cache[key] = [res, time()]
                        return res
                self.cache[key][1] = time()
                return self.cache[key][0]
            else:
                res = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [res, time()]
                    self.cache.move_to_end(key)
                else:
                    self.cache.popitem()
                    self.cache[key] = [res, time()]
                    self.cache.move_to_end(key)
                return res
        return wrapper
