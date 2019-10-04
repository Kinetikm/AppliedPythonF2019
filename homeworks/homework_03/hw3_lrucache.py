#!/usr/bin/env python
# coding: utf-8

from time import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.cach_args = {}
        self.cach_time = {}

    def __call__(self, func):
        def cach(*args, **kwargs):
            temp = ((args, str(kwargs)))
            if temp in self.cach_args:
                if self.ttl is not None and (time() - self.cach_time[temp])*1000 > self.ttl:
                    result = func(*args, **kwargs)
                    self.cach_args[temp] = result
                    self.cach_time[temp] = time()
                else:
                    result = self.cach_args[temp]
            else:
                result = func(*args, **kwargs)
                if len(self.cach_args) >= self.maxsize:
                    for arg, time_ in self.cach_time.items():
                        max_ = time_
                        key = arg
                        if time_ < max_:
                            max_ = time_
                            key = arg
                    self.cach_args.pop(key)
                self.cach_args[temp] = result
                self.cach_time[temp] = time()
            return result
        return cach
