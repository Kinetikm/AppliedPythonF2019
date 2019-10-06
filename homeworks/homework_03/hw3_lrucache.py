#!/usr/bin/env python
# coding: utf-8

import time
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.results = OrderedDict()
        self.time_in_cache = OrderedDict()

    def clean_tail(self, *args):
        self.results.popitem(*args)
        self.time_in_cache.popitem(*args)

    def refresh(self, arg, result):
        self.results[arg] = result
        self.time_in_cache[arg] = time.time()

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        list = args
        if self.results.get(list):
            if self.ttl < (time.time() - self.time_in_cache[list]):
                self.clean_tail(list)
                new_result = function(*args, **kwargs)
                self.refresh(list, new_result)
                return new_result
            return self.results[list]
        else:
            if self.maxsize <= len(self.function_result):
                self.clean_tail(list)
            new_result = function(*args, **kwargs)
            self.refresh(list, new_result)
            return new_result
