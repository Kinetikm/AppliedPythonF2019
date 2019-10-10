#!/usr/bin/env python
# coding: utf-8
from time import time


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
            if key not in self.cache['key_value'] or (
                    self.ttl and (time() - self.cache['time'][key]) * 1000 > self.ttl):
                self.check_size()
                out = func(*args, **kwargs)
                self.cache['key_value'][key] = out
                self.cache['time'][key] = time()
            else:
                self.cache['time'][key] = time()
                out = self.cache['key_value'][key]
                self.check_size()
            return out

        return inner

    def check_size(self):
        if len(self.cache['key_value']) > self.maxsize:
            key_del = min(self.cache['time'], key=self.cache['time'].get)
            del self.cache['key_value'][key_del]
            del self.cache['time'][key_del]
