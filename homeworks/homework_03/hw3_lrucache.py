#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        #  TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}

    def __call__(self, func):
        def inner_func(*args, **kwargs):
            self.func = func
            key = (args, tuple(kwargs))
            if key not in self.cache:
                if len(self.cache) < self.maxsize:
                    self.cache[key] = [self.func(*args, **kwargs), time.time()]
                else:
                    max = 0
                    for i in self.cache:
                        if (time.time() - self.cache[i][1]) > max:
                            max = time.time() - self.cache[i][1]
                            key_max = i
                    self.cache.pop(key_max)
                    self.cache[key] = [self.func(*args, **kwargs), time.time()]
                return self.cache[key][0]
            else:
                if self.ttl is not None:
                    if (time.time() - self.cache[key][1])*1000 > self.ttl:
                        self.cache.pop(key)
                        self.cache[key] = [self.func(*args, **kwargs), time.time()]
                        return self.func(*args, **kwargs)
                self.cahe[key][1] = time.time()
                return self.cache[key][0]
        return inner_func
