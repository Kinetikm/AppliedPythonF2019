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
        self.time_in_cache = {}
        self.args_in_cache = {}

    def __call__(self, func):
        # TODO вызов функции
        def lrucache(*args, **kwargs):
            point = ((args, str(kwargs)))
            if point in self.args_in_cache:
                if self.ttl is not None and (time() - self.time_in_cache[point]) * 1000 > self.ttl:
                    result = func(*args, **kwargs)
                    self.time_in_cache[point] = time()
                    self.args_in_cache[point] = result
                else:
                    result = self.args_in_cache[point]
            else:
                result = func(*args, **kwargs)
                if len(self.args_in_cache) >= self.maxsize:
                    max_time = -1
                    for (argument, Time) in self.time_in_cache.items():
                        if Time > max_time:
                            max_time = Time
                            key = argument
                    self.args_in_cache.pop(key)
                self.time_in_cache[point] = time()
                self.args_in_cache[point] = result
            return result
        return lrucache
