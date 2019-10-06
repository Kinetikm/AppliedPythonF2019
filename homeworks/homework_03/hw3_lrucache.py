#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.times = {}
        self.size = 0
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        raise NotImplementedError

    def _make_key(self, args, kwargs):
        key = args
        if kwargs:
            key += kwargs
        return key

    def __call__(self, func):
        def cache(*args, **kwargs):
            key = self._make_key(args, kwargs)
            if key in self.cache:
                if self.ttl is not None and time.time() - self.times[key] < self.ttl:
                    self.times[key] = time.time()
                    return self.cache[key]
                elif self.ttl is None:
                    self.times[key] = time.time()
                    return self.cache[key]
            res = func(*args, **kwargs)
            if self.size == self.maxsize:
                del_key = min(self.times, key=self.times.get)
                del self.cache[del_key]
                del self.times[del_key]
                self.size -= 1
            self.times[key] = time.time()
            self.cache[key] = res
            self.size += 1
            return res
        return cache
