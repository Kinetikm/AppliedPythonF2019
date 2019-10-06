#!/usr/bin/env python
# coding: utf-8

import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self._ttl = ttl
        self._maxsize = maxsize
        self._cache = {}  # { key : (time, value) }

    def _cache_gc(self):
        if len(self._cache) < self._maxsize:
            return
        del_list = []
        min_t_key = list(self._cache.keys())[0]
        min_t = list(self._cache.values())[0][0]
        for key, value in self._cache.items():
            f_add_time, _ = value
            if f_add_time < min_t:
                min_t = f_add_time
                min_t_key = key
            if self._ttl is not None and (time.time() - f_add_time) * 1000 <= self._ttl:
                del_list.append(key)
        if len(del_list) > 0:
            for item in del_list:
                self._cache.pop(item)
        else:
            self._cache.pop(min_t_key)

    def __call__(self, function):

        def wrapper(*args, **kwargs):
            cache_key = tuple((args, tuple(kwargs)))
            if cache_key in self._cache:
                f_add_time, f_result = self._cache[cache_key]
                if self._ttl is None:
                    self._cache[cache_key] = (time.time(), f_result)
                if self._ttl is None or (time.time() - f_add_time) * 1000 <= self._ttl:
                    return f_result
            else:
                self._cache_gc()
            f_result = function(*args, **kwargs)
            self._cache[cache_key] = (time.time(), f_result)
            return f_result

        return wrapper
