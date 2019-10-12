#!/usr/bin/env python
# coding: utf-8
import time
from collections import OrderedDict as dct


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl=300):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.store = dct([])

    def __call__(self, function):
        def wrap(*args, **kwargs):
            if len(self.store) > self.maxsize:
                        self.store.popitem(last=False)
            t = tuple([x for x in args] + [x for x in kwargs.items()] + [None])
            if self.ttl is None:
                if t in self.store:
                    tmp = self.store.pop(t)
                    self.store[t] = tmp
                    return tmp
                else:
                    print(self.store)
                    self.store[t] = (function(*args, **kwargs), 0)
                    return self.store[t]
            if t in self.store and \
                    time.time() - self.store[t][1] <= self.ttl:
                tmp = self.store.pop(t)
                self.store[t] = tmp
                return tmp[0]
            self.store[t] = (function(*args, **kwargs), time.time(), self.ttl)
            return self.store[t][0]
        return wrap
