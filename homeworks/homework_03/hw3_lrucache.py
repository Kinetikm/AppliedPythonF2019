#!/usr/bin/env python
# coding: utf-8


import time
import collections
import functools

class LRUCacheDecorator:
    
    class CacheEntity:
        def __init__(self, function, arguments=(), kw_arguments=dict(), ttl=None):
            self.last_use_time = time.time()
            # self.ttl = None if ttl is None else ttl / 1000
            self.ttl = ttl
            self.function = function
            self.arguments = arguments
            self.kw_arguments = kw_arguments
            self.result = None
            self.recalc_result()

        def expired(self):
            if self.ttl is None:
                return False
            return self.ttl < time.time() - self.last_use_time

        def get_result(self):
            if self.expired():
                self.recalc_result()
            self.last_use_time = time.time()
            return self.result

        def recalc_result(self):
            self.result = self.function(*self.arguments, **self.kw_arguments)

        def __eq__(self, other):
            return self.last_use_time == other.last_use_time

        def __lt__(self, other):
            return self.last_use_time < other.last_use_time

        def __repr__(self):
            return "{} {}".format(self.ttl, self.last_use_time)

    def __init__(self, maxsize=3, ttl=None):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.calls = collections.OrderedDict()

    def __call__(self, func):

        @functools.wraps(func)
        def cached_call(*args, **kwargs):
            cached_calls = self.calls

            args_key = (args, frozenset(kwargs.items()))

            if args_key in cached_calls:
                cached_calls.move_to_end(args_key, last=True)
                return cached_calls[args_key].get_result()
            else:
                if len(cached_calls) >= self.maxsize:
                    cached_calls.popitem(last=False)
                ce = self.CacheEntity(func, arguments=args, kw_arguments=kwargs, ttl=self.ttl)
                cached_calls[args_key] = ce

        return cached_call
