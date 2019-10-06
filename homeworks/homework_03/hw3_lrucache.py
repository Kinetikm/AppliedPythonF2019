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
        self.maxsize = maxsize
        self.ttl = ttl
        self.time_in_cache = {}
        self.args_in_cache = {}

    def __call__(self, func):
        # TODO вызов функции
        def lrucache(*args, **kwargs):
            index = ((args, str(kwargs)))
            if index in self.args_in_cache:
                if self.ttl is not None and (time() - self.time_in_cache[index]) * 1000 > self.ttl:
                    res = func(*args, **kwargs)
                    self.time_in_cache[index] = time()
                    self.args_in_cache[index] = res
                else:
                    res = self.args_in_cache[index]
            else:
                res = func(*args, **kwargs)
                if len(self.args_in_cache) >= self.maxsize:
                    max_time = -1
                    for (arg, current_time) in self.time_in_cache.items():
                        if current_time > max_time:
                            max_time = current_time
                            key = arg
                    self.args_in_cache.pop(key)
                self.time_in_cache[index] = time()
                self.args_in_cache[index] = res
            return res
        return lrucache
