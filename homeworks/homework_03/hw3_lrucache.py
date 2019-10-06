#!/usr/bin/env python
# coding: utf-8

from time import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время(мс), через которое кеш должен исчезнуть
        '''
        self._maxsize = maxsize
        self._ttl = ttl
        self._cache = {}
        self._time = {}

    def __call__(self, func):
        def internal(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in self._cache:
                if len(self._cache) >= self._maxsize:
                    oldest_key = sorted(self._time.items(), key=lambda x: x[1])[0][0]
                    del self._cache[oldest_key]
                    del self._time[oldest_key]
                result = func(*args, **kwargs)
                self._cache[key] = result
                self._time[key] = time()
            else:
                if self._ttl and (time() - self._time[key]) * 1000 > self._ttl:
                    result = func(*args, **kwargs)
                    self._time[key] = time()
                    self._cache[key] = result
                else:
                    self._time[key] = time()
                    result = self._cache[key]
            return result
        return internal
