#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.time_in_cache = {}
        self.args_in_cache = {}

    def __call__(self, func):
        def lrucache(*args, **kwargs):
            indx = ((args, str(kwargs)))
            if indx in self.args_in_cache:
                if self.ttl is not None and (time() - self.time_in_cache[indx]) * 1000 > self.ttl:
                    res = func(*args, **kwargs)
                    self.time_in_cache[indx] = time()
                    self.args_in_cache[indx] = res
                else:
                    res = self.args_in_cache[indx]
            else:
                res = func(*args, **kwargs)
                if len(self.args_in_cache) >= self.maxsize:
                    max_time = -1
                    for (arg, current_time) in self.time_in_cache.items():
                        if current_time > max_time:
                            max_time = current_time
                            key = arg
                    self.args_in_cache.pop(key)
                self.time_in_cache[indx] = time()
                self.args_in_cache[indx] = res
            return res
        return lrucache
