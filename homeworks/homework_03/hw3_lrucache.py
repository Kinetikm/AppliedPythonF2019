#!/usr/bin/env python
# coding: utf-8
from time import time, sleep


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.ttl = ttl
        self.maxsize = maxsize
        self.cache = {}
        self.time = 0

    def __call__(self, func):
        def inner(*args, **kwargs):
            key_tup = args, kwargs
            key = str(key_tup)
            if key in self.cache:
                item_time = self.cache[key][2]
                if self.ttl and (time() - item_time) * 1000 > self.ttl:
                    del self.cache[key]
                elif self.ttl and (time() - item_time) * 1000 < self.ttl:
                    item = self.cache[key]
                    del self.cache[key]
                    self.cache[key] = item[0], item[1], time()
                    return item[1]
                else:
                    item = self.cache[key]
                    del self.cache[key]
                    self.cache[key] = item[0], item[1], time()
                    return item[1]
            ret = func(*args, **kwargs)
            if len(self.cache.keys()) >= self.maxsize:
                self.delete_most_old()
            self.cache[key] = key, ret, time()
            return ret
        self.time = time()
        return inner

    def delete_most_old(self):
        time_old = time()
        for key in self.cache.keys():
            if self.cache[key][2] < time_old:
                time_old = self.cache[key][2]
                key_old = key
        del self.cache[key_old]
