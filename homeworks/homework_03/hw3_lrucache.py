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
        self.ttl = ttl
        self.maxsize = maxsize
        self.cash = {}
        self.time = {}
        raise NotImplementedError

    def __call__(self, func):
        def f( *args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in self.cash:
                if len(self.cash) == self.maxsize:
                    keys = list(self.cash.keys())
                    values = list(self.cash.values())
                    values.sort()
                    values.reverse()
                    del_value = values[0]
                    self.keys.pop(keys[list(self.cash.values()).index(del_value)])
                    self.time.pop(keys[list(self.cash.values()).index(del_value)])
                value = func(*args, **kwargs)
                self.time[key] = time.time()
                self.cash[key] = value
                return value
            else:
                if time.teme() - self.time[key] > self.ttf:
                    value = func( *args, **kwargs)
                    self.time[key] = time.time()
                    self.cash[key] = value
                    return value
                else:
                    return self.cash[key]
        return f
        raise NotImplementedError
