#!/usr/bin/env python
# coding: utf-8
from time import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.maxsize = maxsize
        self.ttl = ttl / 1000 if ttl else None
        self.cache = {
            'key_value': OrderedDict(),
            'time': OrderedDict()
        }

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = hash(str(args) + str(kwargs))
            if key not in self.cache['key_value'] or (
                    self.ttl and (time() - self.cache['time'][key]) > self.ttl):
                out = func(*args, **kwargs)
                self.cache['key_value'][key] = out
                self.cache['time'][key] = time()
                self.check_size()
            else:
                self.cache['time'][key] = time()
                out = self.cache['key_value'][key]
                self.check_size()
            return out

        return inner

    def check_size(self):
        if len(self.cache['key_value']) > self.maxsize:
            item_del = self.cache['time'].popitem(last=False)
            del self.cache['key_value'][item_del[0]]
