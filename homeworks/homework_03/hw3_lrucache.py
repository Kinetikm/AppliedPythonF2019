#!/usr/bin/env python
# coding: utf-8

from time import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.cache = dict()
        self.cache_time = dict()
        self.maxsize = maxsize
        self.ttl = ttl
        
    def __call__(self, func):
        def _dec(*args, **kwargs):
            number = str(args) + str(*kwargs)
            num_ = number[0]
            if  num_ in self.cache: 
                if (time.time() - self.cache_time[num_]) * 1000 < self.ttl and self.ttl is not None:
                    return self.cache[num_]
                else:
                    self.cache[num_] = func(*args, **kwargs)
                    self.cache_time[num_] = time.time()
            if len(self.cache) >= self.maxsize:
                for num in self.cache_time:
                    if self.cache_time[num] == sorted(self.cache_time.values(), reserve=True)[0]:
                        self.cache_time.pop(num)
                        self.cache.pop(num)
                        self.cache[num_] = func(*args, **kwargs)
                        self.cache_time[num_] = time.time()
            return self.cache[num_]
        return _dec
