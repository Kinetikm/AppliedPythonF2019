#!/usr/bin/env python
# coding: utf-8
import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
		self.ttl = ttl
		if self.ttl:
		    self.ttl = ttl / 1000
        self.cache = OrderedDict()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = hash(str(args) + str(tuple(kwargs)) + str(tuple(kwargs.values())))
            if key not in self.cache:
                result = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [result, time.time()]
                else:
                    self.cache.popitem(last=False)
                    self.cache[key] = [result, time.time()]
                return result
            else:
                if self.ttl:
                    if (time.time() - self.cache[key][1]) > self.ttl:
                        result = func(*args, **kwargs)
                        self.cache[key][0] = result
                        return result
                self.cache.move_to_end(key, last=True)
                self.cache[key][1] = time.time()
                return self.cache[key][0]
        return wrapper

