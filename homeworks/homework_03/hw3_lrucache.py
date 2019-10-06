#!/usr/bin/env python
# coding: utf-8

from time import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        if isinstance(maxsize, int):
            self.size = maxsize
        else:
            self.size = 1024
        if isinstance(ttl, (int, float)):
            self.ttl = ttl
        else:
            self.ttl = 10 ** 6

    def __call__(self, function):
        cache = dict()

        def wrapper(*args, **kwargs):
            arghash = hash(tuple([*args, *kwargs]))
            if arghash not in cache:
                if len(cache) < self.size:
                    cache[arghash] = [function(*args, **kwargs), time() * 1000, time() * 1000]
                else:
                    self.delete_record(cache)
                    cache[arghash] = [function(*args, **kwargs), time() * 1000, time() * 1000]
            else:
                if time() * 1000 - cache[arghash][1] > self.ttl:
                    cache[arghash] = [function(*args, **kwargs), time() * 1000, time() * 1000]
                else:
                    cache[arghash][2] = time() * 1000
            return cache[arghash][0]
        return wrapper

    def delete_record(self, cache):
        max_time_unused = time() * 1000
        key_of_max = None
        for i, value in cache.items():
            if value[2] < max_time_unused:
                max_time_unused = value[2]
                key_of_max = i
        del cache[key_of_max]
