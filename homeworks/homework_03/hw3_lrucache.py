#!/usr/bin/env python
# coding: utf-8

import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.cache = dict()
        self.cache_time = dict()
        self.maxsize = maxsize
        self.ttl = ttl

    def __call__(self, func):
        def _dec(*args, **kwargs):
            number = str(args) + str(*kwargs)
            num_ = number[1]
            if num_ in self.cache:
                if self.ttl is not None and (time.time() - self.cache_time[num_]) * 1000 <= self.ttl:
                    self.cache_time[num_] = time.time()
                    val = self.cache[num_]
                    return val
                else:
                    val = func(*args, **kwargs)
                    self.cache[num_] = val
                    self.cache_time[num_] = time.time()
                    return val
            elif len(self.cache) == self.maxsize:
                for num in self.cache_time:
                    if self.cache_time[num] == sorted(self.cache_time.values())[0]:
                        self.cache_time.pop(num)
                        self.cache.pop(num)
                        break
            val = func(*args, **kwargs)
            self.cache[num_] = val
            self.cache_time[num_] = time.time()
            return val
        return _dec
