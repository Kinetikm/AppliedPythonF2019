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
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.now_time = 0

    def __call__(self, func, *args, **kwargs):
        def dec(*args, **kwargs):
            if self.ttl is not None:
                self.now_time = time.time() * 1000
                for key in [key for key, val in self.cache.items() if self.now_time - val[0] >= self.ttl]:
                    del self.cache[key]
            # TODO вызов функции

            if args in self.cache:
                self.now_time = time.time() * 1000
                self.cache[args] = (self.now_time, self.cache.pop(args)[1])
                return self.cache[args][1]

            if len(self.cache) == self.maxsize:
                del self.cache[list(self.cache.keys())[0]]
            result = func(*args, **kwargs)
            self.now_time = time.time() * 1000
            self.cache[args] = (self.now_time, result)
            return result

        return dec
