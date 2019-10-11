#!/usr/bin/env python
# coding: utf-8

from time import time
from functools import wraps


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        if ttl is not None:
            self.ttl = ttl/1000
        else:
            self.ttl = ttl
        self.cach_args = {}

    def __call__(self, func):
        @wraps(func)
        def func_cach(*args, **kwargs):
            temp = ((args, str(kwargs)))
            if temp in self.cach_args:
                if self.ttl is not None and (time() - self.cach_args[temp][1]) > self.ttl:
                    result = func(*args, **kwargs)
                    self.cach_args.pop(temp)
                    self.cach_args[temp] = [result, time()]
                else:
                    result = self.cach_args[temp][0]
                    self.cach_args.pop(temp)
                    self.cach_args[temp] = [result, time()]
            else:
                result = func(*args, **kwargs)
                if len(self.cach_args) >= self.maxsize:
                    self.cach_args.pop(list(self.cach_args.keys())[0])
                self.cach_args[temp] = [result, time()]
            return result
        return func_cach
