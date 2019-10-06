#!/usr/bin/env python
# coding: utf-8
from collections import OrderedDict
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
        self.cache = OrderedDict()
        self.maxsize = maxsize
        self.ttl = ttl
        self.mode = "decorating"

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        if self.mode == "decorating":
            self.function = args[0]
            self.mode = "calling"
            return self
        for i in args:
            print(i)
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        key = (*args, *kwargs)
        if self.ttl:
            if key in self.cache and time.time() - self.cache[key][1] < self.ttl:
                result = self.cache[key]
                del self.cache[key]
                self.cache[key] = result
                return result[0]
            else:
                self.cache[key] = [self.function(*args, **kwargs), time.time()]
                return self.cache[key][0]
        if key in self.cache:
            result = self.cache[key]
            del self.cache[key]
            self.cache[key] = result
            return result[0]
        self.cache[key] = [self.function(*args, **kwargs), time.time()]
        return self.cache[key][0]
