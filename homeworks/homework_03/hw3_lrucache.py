#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, function, *, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.results = {}
        self.calculated = 0
        self.maxsize = maxsize
        self.ttl = ttl
        self.function = function

    def lru_del(self, call_time):
        if self.calculated <= 1:
            self.results = {}
            self.calculated = 0
            return
        last = (call_time,None)
        for key in self.results:
            if self.results[key][0] < last[0]:
                last = (self.results[key][0], key)
        del self.results[last[1]]
        self.calculated -= 1

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        call_time = time.time()
        res = None
        if (args, kwargs) in self.results:
            if self.ttl is None or (call_time - self.results[(args, kwargs)][0]) * 1000 < self.ttl:
                res = self.results[(args, kwargs)]
                self.results[(args, kwargs)] = (call_time, res)
                return res
            else:
                res = self.function(*args, **kwargs)
                self.results[(args, kwargs)] = (call_time, res)
        if self.calculated < self.maxsize:
            self.results[(args, kwargs)] = (call_time, res)
        else:
            res = self.function(*args, **kwargs)
            if self.calculated < self.maxsize:
                self.results[(args, kwargs)] = (call_time, res)
            else:
                self.lru_del(call_time)
                self.results[(args, kwargs)] = (call_time, res)
        return res
