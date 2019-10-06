#!/usr/bin/env python
# coding: utf-8

import collections
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
        self.cache = collections.OrderedDict()
        self.timings = {}

    def __call__(self, func):
        # TODO вызов функции

        def inner(*args):
            present_time = time.time()
            if args in self.cache:
                if self.ttl and ((present_time - self.timings[args]) > self.ttl):
                    result = func(*args)
                    del self.cache[args]
                    self.cache[args] = result
                    self.timings[args] = present_time
                    if len(self.cache) > self.maxsize:
                        self.cache.popitem(last=False)
                else:
                    result = self.cache[args]
                    self.cache.move_to_end(args)
            else:
                result = func(*args)
                self.cache[args] = result
                self.timings[args] = present_time
                if len(self.cache) > self.maxsize:
                    del self.timings[self.cache.popitem(last=False)[0]]
            return result

        return inner
