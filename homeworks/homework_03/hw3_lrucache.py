#!/usr/bin/env python
# coding: utf-8

import time
from collections import OrderedDict
from functools import wraps


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.function_result = OrderedDict()
        self.time_in_cache = OrderedDict()

    def del_old(self, *args):
        self.function_result.popitem(*args)
        self.time_in_cache.popitem(*args)

    def update_cache(self, arg, result):
        self.function_result[arg] = result
        self.time_in_cache[arg] = time.time()

    def __call__(self, function):
        @wraps(func)
        def lru_function(*args, **kwargs):
            t = tuple([x for x in args] + [x for x in kwargs.items()] + [None])
            if self.function_result.get(t):
                if self.ttl is not None:
                    if self.ttl < (time.time() - self.time_in_cache[t]):
                        self.del_old(t)
                        newresult = function(*args, **kwargs)
                        self.update_cache(t, newresult)
                        return newresult
                    return self.function_result[t]
            else:
                if self.maxsize > len(self.function_result):
                    newresult = function(*args, **kwargs)
                    self.update_cache(t, newresult)
                    return newresult
                else:
                    self.del_old()
                    newresult = function(*args, **kwargs)
                    self.update_cache(t, newresult)
                    return newresult
        return lru_function
