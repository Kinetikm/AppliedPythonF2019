#!/usr/bin/env python
# coding: utf-8


import time
# from heapq import heappush, heappop
from typing import Set, Any


class LRUCacheDecorator:

    class CacheEntity:
        def __init__(self, function, arguments=(), ttl = None):
            self.last_use_time = time.time()
            self.ttl = ttl
            self.function = function
            self.arguments = arguments
            self.result = None
            self.recalc_result()

        def expired(self):
            if self.ttl is None:
                return False
            return self.ttl > time.time() - self.last_use_time

        def get_result(self):
            if self.expired():
                self.recalc_result()
            self.last_use_time = time.time()
            return self.result

        def recalc_result(self):
            self.result = self.function(*self.arguments)

        def __eq__(self, other):
            return self.last_use_time == other.last_use_time

        def __lt__(self, other):
            # print("other", other)
            return self.last_use_time < other.last_use_time


    def __init__(self, maxsize=3, ttl=None):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.funcs = dict()

    def __call__(self, func):

        cached_calls: Set[LRUCacheDecorator.CacheEntity] = dict()  # todo use heap
        self.funcs[func] = cached_calls

        def cached_call(*args, **kwargs):
            cached_calls = self.funcs[func]
            if args in cached_calls:
                return cached_calls[args].get_result()
            else:
                # print(cached_calls)
                if len(cached_calls) >= self.maxsize:
                    oldest_used = sorted(cached_calls.values())[0]
                    del cached_calls[oldest_used.arguments]
                ce = LRUCacheDecorator.CacheEntity(func, arguments=args, ttl=self.ttl)
                cached_calls[args] = ce

        return cached_call