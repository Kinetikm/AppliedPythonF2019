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
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cashe = {}  # {hash: [result fuc(), time of call], ...}

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        func = args[0]

        @wraps(func)
        def inner(*args, **kwargs):
            h = hash(str(args) + str(kwargs))
            if h in self.cashe:
                if self.ttl is None or (time.time() - self.cashe[h][1]) * 1000 < self.ttl:
                    self.cashe[h][1] = time.time()
                    return self.cashe[h][0]

            if len(self.cashe) == self.maxsize:
                del[self.cashe[min(self.cashe, key=lambda x: self.cashe[x][1])]]

            res = func(*args, **kwargs)
            self.cashe[h] = [res, time.time()]
            return res
        return inner
