#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:

    class Results():
        def __init__(self, res, time):
            self.result = res
            self.time = time

    def __init__(self, maxsize, ttl):
        '''
            :param maxsize: максимальный размер кеша
            :param ttl: время в млсек, через которое кеш
            должен исчезнуть
            '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.size = maxsize
        self.ttl = ttl
        self.cache = dict()

    def get_key(self, *args, **kwargs):
        s = ''.join(str(arg) for arg in args)
        s.join(str(kwarg) for kwarg in kwargs)
        return s

    def __call__(self, func):
        # TODO вызов функции
        def inner(*args, **kwargs):
            key = self.get_key(*args, **kwargs)
            if key in self.cache:
                if self.ttl:
                    if (time() - self.cache[key].time)*1000 > self.ttl:
                        del self.cache[key]
                        result = func(*args, **kwargs)
                        self.cache[key] = self.Results(result, time())
                        return result
                self.cache[key].time = time()
                return self.cache[key].result
            else:
                result = func(*args, *kwargs)
                if len(self.cache) < self.size:
                    self.cache[key] = self.Results(result, time())
                else:
                    minkey = min(self.cache,  key=lambda x: self.cache[x].time)
                    del self.cache[minkey]
                    self.cache[key] = self.Results(result, time())
                return result
        return inner
