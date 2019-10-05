#!/usr/bin/env python
# coding: utf-8
import time
from functools import wraps


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.results = {}
        self.calculated = 0
        self.maxsize = maxsize
        self.ttl = ttl
        self.function = None

    def lru_del(self):
        if self.calculated <= 1:
            self.results = {}
            self.calculated = 0
            return
        last = (time.time(), None)
        for key in self.results:
            if self.results[key][0] < last[0]:
                last = (self.results[key][0], key)
        del self.results[last[1]]
        self.calculated -= 1

    def __call__(self, function, *ar, **kw):
        self.function = self.function or function

        @wraps(function)
        def f(*args, **kwargs):
            call_time = time.time()
            res = None
            key = (args, tuple(kwargs.items()))
            if key in self.results:
                if self.ttl is None or (call_time - self.results[key][0]) * 1000 < self.ttl:
                    res = self.results[key][1]
                    self.results[key] = (call_time, res)
                    return res
                else:
                    res = self.function(*args, **kwargs)
                    call_time = time.time()
                    self.results[key] = (call_time, res)
                    return res
            else:
                res = self.function(*args, **kwargs)
                call_time = time.time()
                if self.calculated < self.maxsize:
                    self.results[key] = (call_time, res)
                    self.calculated += 1
                else:
                    self.lru_del()
                    self.results[key] = (call_time, res)
                    self.calculated += 1
            return res
        return f
