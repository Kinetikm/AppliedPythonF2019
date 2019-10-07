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
        self.cache = {}
        self.cache_time = {}

    def __call__(self, func):
        # TODO вызов функции
        def inner(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in self.cache:
                if len(self.cache) == self.maxsize:
                    later_time = time()
                    for k in self.cache_time:
                        if self.cache_time[k] < later_time:
                            later_time = self.cache_time[k]
                            del_key = k
                    del self.cache[k]
                    del self.cache_time[k]
                self.cache[key] = func(*args, **kwargs)
                self.cache_time[key] = time()
                return self.cache[key]
            else:
                if self.ttl and (time() - self.cache_time[key]) * 1000 > self.ttl:
                    self.cache_time[key] = time()
                    self.cache[key] = func(*args, **kwargs)
                else:
                    self.cache_time[key] = time()
                return self.cache[key]
        return inner
