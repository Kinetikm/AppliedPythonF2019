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
        self.maxsize = maxsize
        self.time = ttl
        self.cache = {}
        self.realsize = 0

    def __call__(self, function):

        def Time():
            return time.time() * 1000

        def internal(*args, **kwargs):
            key = args + tuple(sorted(kwargs.items()))
            if key not in self.cache.keys():
                if self.realsize < self.maxsize:
                    self.realsize += 1
                else:
                    index = min(self.cache.items(),
                                key=lambda i: i[1][1])
                    del self.cache[index[0]]
            else:
                item = self.cache[key]
                print(self.cache)
                if self.time is None or Time() - item[1] <= \
                        self.time:
                    self.cache[key] = (item[0], Time())
                    return item[0]
            self.cache[key] = (function(*args, **kwargs), Time())
            return self.cache[key][0]

        return internal
