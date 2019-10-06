#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:

    class Results():
        def __init__(self, res, time):
            self.result = res
            self.time = time

    def __init__(self, maxsize, ttl):
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        raise NotImplementedError
        self.maxsize = maxsize
        self.time = ttl
        self.cache = {}

    def get_key(self, *args, **kwargs):
        s = ''.join(str(arg) for arg in args)
        s.join(str(kwarg) for kwarg in kwargs)
        return s

    def __call__(self, func):
        # TODO вызов функции
        def inner(*args, **kwargs):
            key = self.get_key(*args, **kwargs)
            if key in self.cache:
                if self.time:
                    if (time() - self.cache[key].time)*1000 > self.time:
                        del self.cache[key]
                        result = func(*args, **kwargs)
                        self.cache[key] = self.Results(result, time())
                        return result
                self.cache[key].time = time()
                return self.cache[key].result
            else:
                result = func(*args, *kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = self.Results(result, time())
                else:
                    minimalkey = min(self.cache, key=lambda x: self.cache[x].time)
                    del self.cache[minimalkey]
                    self.cache[key] = self.Results(result, time())
                return result
        return inner
