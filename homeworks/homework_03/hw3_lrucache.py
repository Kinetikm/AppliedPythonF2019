#!/usr/bin/env python
# coding: utf-8
from time import time


# :)
class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {
            'key_value': {},
            'time': {}
        }

    def __call__(self, func):
        def inner(*args, **kwargs):
            key = hash(str(args) + str(kwargs))
            if key not in self.cache['key_value']:
                if len(self.cache['key_value']) >= self.maxsize:
                    items = sorted(self.cache['time'].items(), key=lambda x: x[1])
                    del self.cache['key_value'][items[0][0]]
                    del self.cache['time'][items[0][0]]
                out = func(*args, **kwargs)
                self.cache['key_value'][key] = out
                self.cache['time'][key] = time()
            elif self.ttl and (time() - self.cache['time'][key]) * 1000 > self.ttl:
                out = func(*args, **kwargs)
                self.cache['time'][key] = time()
            else:
                self.cache['time'][key] = time()
                out = self.cache['key_value'][key]
            return out

        return inner
