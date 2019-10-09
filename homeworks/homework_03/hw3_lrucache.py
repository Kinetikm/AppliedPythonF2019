#!/usr/bin/env python
# coding: utf-8

from time import time
from functools import wraps


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.maxsize = maxsize
        self.ttl = ttl / 1000 if ttl is not None else None
        self.cache = {}
        self.cache_time = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = self._get_hash(args, kwargs)

            if cache_key not in self.cache or self.ttl and time() - self.cache_time[cache_key] > self.ttl:
                res = func(*args, **kwargs)
                self.cache[cache_key] = res
                self.cache_time[cache_key] = time()
            else:
                self.cache_time[cache_key] = time()
                res = self.cache[cache_key]

            self._update_cache_if_maxsize()

            return res

        return wrapper

    def _update_cache_if_maxsize(self):
        if len(self.cache) > self.maxsize:
            oldest_key = self._get_oldest_key(self.cache_time)
            del self.cache[oldest_key]
            del self.cache_time[oldest_key]

    @staticmethod
    def _get_oldest_key(dict_with_time_in_value: dict):
        return min(dict_with_time_in_value, key=dict_with_time_in_value.get)

    @staticmethod
    def _get_hash(args, kwargs):
        return hash(str(args) + str(kwargs))
