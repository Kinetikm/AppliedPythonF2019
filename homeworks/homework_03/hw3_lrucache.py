#!/usr/bin/env python
# coding: utf-8

import time
from collections import OrderedDict

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
        def lru_function(*args, **kwargs):
            list = args
            if self.function_result.get(list):
                if self.ttl is not None:
                    if self.ttl < (time.time() - self.time_in_cache[list]):
                        self.del_old(list)
                        newresult = function(*args, **kwargs)
                        self.update_cache(list, newresult)
                        return newresult
                    else:
                        return self.function_result[list]
                else:
                    return self.function_result[list]
            else:
                if self.maxsize > len(self.function_result):
                    newresult = function(*args, **kwargs)
                    self.update_cache(list, newresult)
                    return newresult
                else:
                    self.del_old(list)
                    newresult = function(*args, **kwargs)
                    self.update_cache(list, newresult)
                    return newresult
        return lru_function


