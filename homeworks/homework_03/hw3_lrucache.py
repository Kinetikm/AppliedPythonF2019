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
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = dict()
        self.time = dict()

    def __call__(self, func):
        def dec(*args, **kwargs):
            k = (args, tuple(kwargs))
            if k in self.cache.keys():
                if self.ttl:
                    if (time.time() - self.time[k]) * 1000 > self.ttl:
                        del self.cache[k]
                        func(*args, **kwargs)
                        self.cache[k] = func(*args, **kwargs)
                        del self.time[k]
                        self.time[k] = time.time()
                        return self.cache[k]
                del self.time[k]
                self.time[k] = time.time()
                return self.cache[k]
            else:
                if self.maxsize:
                    if len(self.cache) < self.maxsize:
                        self.cache[k] = func(*args, **kwargs)
                        self.time[k] = time.time()
                    else:
                        d = max(self.time, key=lambda elem: time.time() - self.time[elem])
                        del self.time[d]
                        del self.cache[d]
                        self.cache[k] = func(*args, **kwargs)
                        self.time[k] = time.time()
                return self.cache[k]
        return dec
