#!/usr/bin/env python
# coding: utf-8
import time
from functools import wraps

class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self._maxsize = maxsize
        self._ttl = ttl
        if ttl is not None:
            self._ttl /= 1000
        self._cache = {}

    def __call__(self, func):
        @wraps(func)
        def _inner_function(*args, **kwargs):
            key = (args, tuple(kwargs))
            if key not in self._cache:
                result = func(*args, **kwargs)
                if len(self._cache) < self._maxsize:
                    self._cache[key] = [result, time.time()]
                else:
                    # FIXED: помним, что dict -- это OrderedDict, и все становится проще и быстрее)))
                    self._cache.pop(list(self._cache.keys())[0])
                    self._cache[key] = [result, time.time()]
                return result
            else:
                if not(self._ttl is None):
                    if (time.time() - self._cache[key][1]) > self._ttl:
                        result = func(*args, **kwargs)
                        self._cache.pop(key)
                        self._cache[key] = [result, time.time()]
                        return result
                res_tmp = self._cache.pop(key)[0]
                self._cache[key] = [res_tmp, time.time()]
                result = self._cache[key][0]
                return result
        return _inner_function
