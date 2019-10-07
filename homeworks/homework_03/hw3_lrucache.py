#!/usr/bin/env python
# coding: utf-8


from time import time


def make_key(args, kwargs):
    key = args
    if kwargs:
        for item in kwargs.items():
            key += item
    return key


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = {}
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/

    def __call__(self, func):
        # TODO вызов функции
        def cache(*args, **kwargs):
            key = make_key(args, kwargs)
            if key in self.cache:
                if self.ttl is not None and (time() - self.cache[key][1]) * 1000 > self.ttl:
                    result = func(*args, **kwargs)
                    self.cache[key] = [result, time()]
                else:
                    result = self.cache[key][0]
                    self.cache[key][1] = time()
            else:
                result = func(*args, **kwargs)
                if len(self.cache) >= self.maxsize:
                    min_time = time()
                    for key_ in self.cache.keys():
                        maybe_min_time = self.cache[key_][1]
                        if maybe_min_time < min_time:
                            min_time = maybe_min_time
                            drop_key = key_
                    del self.cache[drop_key]
                self.cache[key] = [result, time()]
            return result
        return cache
