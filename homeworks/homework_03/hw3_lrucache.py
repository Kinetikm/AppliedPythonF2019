#!/usr/bin/env python
# coding: utf-8

import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть"""
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.sentinel = object()

    def __call__(self, func):
        if self.maxsize == 0:
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
        else:
            def wrapper(*args, **kwargs):
                key = (args, tuple(kwargs))
                result = self.cache.get(key, (self.sentinel, ))
                if result[0] is not self.sentinel:
                    if self.ttl is not None:
                        if (time.time() - result[1]) * 1000 <= self.ttl:
                            self.cache[key] = (result[0], time.time())
                            return result[0]
                        else:
                            self.cache.pop(key)
                    else:
                        self.cache[key] = (result[0], time.time())
                        return result[0]
                result = func(*args, **kwargs)
                self.cache[key] = (result, time.time())
                if len(self.cache.keys()) > self.maxsize:
                    min_k, min_t = None, None
                    for k in self.cache.keys():
                        if min_t:
                            if min_t > self.cache[k][1]:
                                min_t = self.cache[k][1]
                                min_k = k
                        else:
                            min_t = self.cache[k][1]
                            min_k = k
                    self.cache.pop(min_k)
                return result
        return wrapper
