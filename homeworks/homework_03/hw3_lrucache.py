#!/usr/bin/env python
# coding: utf-8

import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        #  инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()

    def __call__(self, func):
        #  вызов функции
        @wraps(func)
        def new_func(*args, **kwargs):
            key = self._hash_args(args, kwargs)
            if key in self.cache:
                ent = self.cache[key]
                if self.ttl is None or time.time() - ent['time'] < self.ttl:
                    del self.cache[key]
                    self.cache[key] = {
                        "result": ent['result'], "time": time.time()}
                    return ent['result']
                ent = self.cache[key]
            if len(self.cache) == self.maxsize:
                self.cache.popitem(last=False)
            result = func(*args, **kwargs)
            self.cache[key] = {"result": result, "time": time.time()}
            return result
        return new_func

    def _hash_args(self, args, kwargs):
        return hash(str(args) + str(kwargs))
