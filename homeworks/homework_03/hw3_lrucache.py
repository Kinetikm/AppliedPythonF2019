#!/usr/bin/env python
# coding: utf-8

import time
from functools import wraps


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
        self.cache = dict()

    def __call__(self, *args, **kwargs):
        #  вызов функции
        func = args[0]

        def new_func(*args, **kwargs):
            key = self._hash_args(args, kwargs)
            if key in self.cache:
                ent = self.cache[key]
                if self.ttl is None or time.time() - ent['time'] < self.ttl:
                    self.cache[key]['time'] = time.time()
                    return ent['result']
            if len(self.cache) == self.maxsize:
                oldest_time = time.time()
                oldest_entry_key = None
                for _key in self.cache:
                    if self.cache[_key]["time"] < oldest_time:
                        oldest_time = self.cache[_key]['time']
                        oldest_entry_key = _key
                del self.cache[oldest_entry_key]
            result = func(*args, **kwargs)
            self.cache[key] = {"result": result, "time": time.time()}
            return result
        return new_func

    def _hash_args(self, args, kwargs):
        return hash(str(args) + str(kwargs))
