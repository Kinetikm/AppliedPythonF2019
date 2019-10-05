#!/usr/bin/env python
# coding: utf-8
import time

class LRUCacheDecorator:


    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            key = hash(str(args) + str(tuple(kwargs)) + str(tuple(kwargs.values())))
            print(key)
            if key not in self.cache:
                result = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [result, time.time()]
                else:
                    keymax = max(self.cache,  key=lambda x: time.time() - self.cache[x][1])
                    self.cache.pop(keymax)
                    self.cache[key] = [result, time.time()]
                return result
            else:
                if self.ttl:
                    if (time.time() - self.cache[key][1]) * 1000 > self.ttl:
                        self.cache.pop(key)
                        result = func(*args, **kwargs)
                        self.cache[key] = result
                        return result
                    else:
                        self.cache[key][1] = time.time()
                        return self.cache[key][0]
        return wrapper
