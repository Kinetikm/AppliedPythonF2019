#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        def obl(*args, **kwargs):
            key = hash(str(args) + str(tuple(kwargs.values())))
            oldest_key = -1
            if key not in self.cache:
                result = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [result, time.time()]
                else:
                    for i in self.cache:
                        if time.time() - self.cache[i][1] > oldest_key:
                            oldest_key = i
                    self.cache.pop(oldest_key)
                    self.cache[key] = [result, time.time()]
                return result
            else:
                if self.ttl:
                    if (time.time() - self.cache[key][1]) * 1000 > self.ttl:
                        self.cache.pop(key)
                        result = func(*args, **kwargs)
                        self.cache[key] = [result, time.time()]
                        return result
                self.cache[key][1] = time.time()
                return self.cache[key][0]
        return obl
