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
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.ttl = ttl
        self.maxsize = maxsize
        self.cursize = 0
        self.hashTable = dict()

    def __call__(self, func):
        def lru_func(*args, **kwargs):
            key = args + list(sorted(kwargs.items()))
            if key in self.hashTable.keys():
                item = self.hashTable[key]
                if self.ttl is None or (time.time()- item[1]) * 1000 <= self.ttl:
                    self.hashTable[key] = [item[0], time.time()]
                    return item[0]
                else:
                    res = func(*args, **kwargs)
                    self.chashTable[key] = [res, time.time()]
                    return res
            else:
                if self.cursize < self.maxsize:
                    self.cursize += 1
                    res = func(*args, **kwargs)
                    self.hashTable[key] = [res, time.time()]
                    return res
                else:
                    del self.hashTable[min(self.hashTable.items(), key=lambda i: i[1][1])[0]]
                    res = func(*args, **kwargs)
                    self.hashTable[key] = [res, time.time()]
                    return res
        return lru_func
