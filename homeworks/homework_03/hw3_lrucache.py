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
            if key not in self.cache:
                res = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [res, time.time()]
                else:
                    keyold = max(self.cache,  key=lambda x: time.time() - self.cache[x][1])
                    self.cache.pop(keyold)
                    self.cache[key] = [res, time.time()]
                return res
            else:
                if self.ttl:
                    if (time.time() - self.cache[key][1]) * 1000 > self.ttl:
                        res = func(*args, **kwargs)
                        self.cache.pop(key)
                        self.cache[key] = [res, time.time()]
                        return res
                self.cache[key][1] = time.time()
                return self.cache[key][0]
        return obl
