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
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache_args = dict()
        self.cache_time = dict()

    def __call__(self, function):
        def lru_cache(*args, **kwargs):
            args_keys = str(args), str(kwargs)
            if args_keys not in self.cache_args:
                cll = function(*args, **kwargs)
                if len(self.cache_args) >= self.maxsize:
                    min_time = time()
                    for k in self.cache_args.keys():
                        t = self.cache_time[k]
                        if t < min_time:
                            min_time = t
                            key = k
                    self.cache_args.pop(key)
                self.cache_args[args_keys] = cll
                self.cache_time[args_keys] = time()
            else:
                new_time = (time() - self.cache_time[args_keys]) * 1000
                if self.ttl is not None and new_time > self.ttl:
                    cll = function(*args, **kwargs)
                    self.cache_args[args_keys] = cll
                    self.cache_time[args_keys] = time()
                else:
                    cll = self.cache_args[args_keys]
                    self.cache_time[args_keys] = time()
            return cll
        return lru_cache
