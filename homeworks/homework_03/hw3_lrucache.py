#!/usr/bin/env python
# coding: utf-8
import time

class LRUCacheDecorator:

    def __init__(self, maxsize, ttl = None, func):
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
        self.func = func

    def __call__(self, *args, **kwargs):
        #  TODO вызов функции
        key = (args, tuple(kwargs))
        if key not in self.cache:
            if len(self.cache) < self.maxsize:
                self.cache[key] = [self.func(*args, **kwargs), time.time()]
            else:
                max = 0
                for i in self.cache:
                    if (time.time() - self.cache[i][1]) > max:
                        max = time.time() - self.cache[i][1]
                        key_max = k
                self.cache.pop(key_max)
                self.cache[key] = [self.func(*args, **kwargs), time.time()]
            return self.func(*args, **kwargs)
        else:
            if self.ttl is not None:
                if (time.time() - self.cache[key][1])*1000 > self.ttl:
                    self.cache.pop(key)
                    self.cache[key] = [self.func(*args, **kwargs), time.time()]
                    return self.func(*args, **kwargs)
            return self.func(*args, **kwargs)
