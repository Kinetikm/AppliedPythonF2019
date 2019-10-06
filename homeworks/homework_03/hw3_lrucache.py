#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """"
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.bool = False
        if (isinstance(ttl, float)) or (isinstance(ttl, int)):
            self.bool = True
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = {}

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            key = (args, tuple(kwargs))
            if key not in self.cache:
                if len(self.cache) == self.maxsize:
                    late_call_time = time.time() * 1000
                    late_call_key = 0
                    for k in self.cache:
                        if self.cache[k][2] < late_call_time:
                            late_call_time = self.cache[k][2]
                            late_call_key = k
                    del self.cache[late_call_key]
                self.cache[key] = [function(*args, **kwargs),
                                   time.time() * 1000, time.time() * 1000]
            else:
                if self.bool:
                    if time.time() * 1000 - self.cache[key][1] > self.ttl:
                        self.cache[key] = [function(*args, **kwargs),
                                           time.time() * 1000, time.time() * 1000]
                    else:
                        self.cache[key][2] = time.time() * 1000
                else:
                    self.cache[key][2] = time.time() * 1000
            return self.cache[key][0]
        return wrapper
