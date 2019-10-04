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
        self._maxsize = maxsize
        self._ttl = ttl
        self._cache = {}

    def __call__(self, func):
        def _inner_function(*args, **kwargs):
            key = (args, tuple(kwargs))
            if key not in self._cache:
                result = func(*args, **kwargs)
                if len(self._cache) < self._maxsize:
                    self._cache[key] = [result, time.time()]
                else:
                    max_time = -1
                    for k in self._cache:
                        if (time.time() - self._cache[k][1]) > max_time:
                            key_ = k
                            max_time = (time.time() - self._cache[k][1])
                    self._cache.pop(key_)
                    self._cache[key] = [result, time.time()]
                return result
            else:
                if not(self._ttl is None):
                    if (time.time() - self._cache[key][1]) * 1000 > self._ttl:
                        result = func(*args, **kwargs)
                        self._cache.pop(key)
                        self._cache[key] = [result, time.time()]
                        return result
                self._cache[key][1] = time.time()
                result = self._cache[key][0]
                return result
        return _inner_function
