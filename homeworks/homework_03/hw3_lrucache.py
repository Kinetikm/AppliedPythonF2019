#!/usr/bin/env python
# coding: utf-8


import time
import functools


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        if ttl is not None:
            self.ttl = ttl / 1000
        else:
            self.ttl = None
        self.cache_dict = {}    # key: args, value: time

    def __call__(self, func):
        @functools.wraps(func)
        def decor(*args, **kwargs):
            if str([args, kwargs]) not in self.cache_dict:
                if len(self.cache_dict) == self.maxsize:
                    self.cache_dict.popitem()
                result = func(*args, **kwargs)
                self.cache_dict[str([args, kwargs])] = (time.time(), result)
                return result
            else:
                key = str([args, kwargs])
                if self.ttl is not None:
                    if time.time() - self.cache_dict[key][0] > self.ttl:
                        self.cache_dict[key] = (time.time(), func(*args, **kwargs))
                    else:
                        self.cache_dict[key] = (time.time(), self.cache_dict[key][1])
                else:
                    self.cache_dict[key] = (time.time(), self.cache_dict[key][1])
                return self.cache_dict[key][1]
        return decor
