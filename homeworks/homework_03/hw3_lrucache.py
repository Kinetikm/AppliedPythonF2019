#!/usr/bin/env python
# coding: utf-8

import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.time = ttl
        self.cache = {}
        self.size = 0

    def __call__(self, function):
        def decorated(*args, **kwargs):
            key = args + tuple(sorted(kwargs.items()))
            if key not in self.cache.keys():
                if self.size < self.maxsize:
                    self.size += 1
                else:
                    if self.cache.items() < key=lambda i: i[1][1]:
                        index = self.cache.items()
                    else:
                        index = key
                    del self.cache[index[0]]
            else:
                item = self.cache[key]
                print(self.cache)
                if self.time is None or time.time() * 1000 - item[1] <= self.time:
                    self.cache[key] = (item[0], time.time() * 1000)
                    return item[0]
            self.cache[key] = (function(*args, **kwargs), time.time() * 1000)
            return self.cache[key][0]
        return decorated
