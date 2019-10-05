#!/usr/bin/env python
# coding: utf-8

from time import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.cache_time = {}

    def __call__(self, func):
        def cache(*args, **kwargs):
            cache_key = self._get_hash(args, kwargs)

            if cache_key not in self.cache:
                res = func(*args, **kwargs)
                self.cache[cache_key] = res
                self.cache_time[cache_key] = time()
            else:
                if self.ttl and (time() - self.cache_time[cache_key]) * 1000 > self.ttl:
                    res = func(*args, **kwargs)
                    self.cache_time[cache_key] = time()
                    self.cache[cache_key] = res
                else:
                    self.cache_time[cache_key] = time()
                    res = self.cache[cache_key]

            self._update_cache_if_maxsize()

            return res

        return cache

    def _update_cache_if_maxsize(self):
        if len(self.cache) > self.maxsize:
            oldest_key = self._get_oldest_key(self.cache_time)
            del self.cache[oldest_key]
            del self.cache_time[oldest_key]

    @staticmethod
    def _get_oldest_key(dict_with_time_in_value: dict):
        max_time = min(dict_with_time_in_value.values())
        return list(dict_with_time_in_value.keys())[
            list(dict_with_time_in_value.values()).index(max_time)
        ]

    @staticmethod
    def _get_hash(args, kwargs):
        return hash(str(args) + str(kwargs))
