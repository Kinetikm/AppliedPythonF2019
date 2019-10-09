import time
from functools import wraps


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        if ttl:
            self.ttl = ttl / 1000
        self.cache = {}
        self.time_ = {}

    def __call__(self, func):
        @wraps(func)
        def cashing(*args, **kwargs):
            key_arg = (args, str(kwargs))
            if key_arg in self.cache:
                t = time.time()
                if self.ttl and (t - self.time_[key_arg]) > self.ttl:
                    res = func(*args, **kwargs)
                    del self.cache[key_arg]
                    del self.time_[key_arg]
                    self.cache[key_arg] = res
                    self.time_[key_arg] = time.time()

                elif self.ttl and (t - self.time_[key_arg]) < self.ttl:
                    res = self.cache.pop(key_arg)
                    del self.time_[key_arg]
                    self.cache[key_arg] = res
                    self.time_[key_arg] = time.time()
                else:
                    res = self.cache.pop(key_arg)
                    self.cache[key_arg] = res
                return res
            else:
                res = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key_arg] = res
                    if self.ttl:
                        self.time_[key_arg] = time.time()

                else:
                    for key in self.cache:
                        del self.cache[key]
                        if self.ttl:
                            del self.time_[key]
                        break
                    self.cache[key_arg] = res
                    if self.ttl:
                        self.time_[key_arg] = time.time()
                return res
        return cashing
