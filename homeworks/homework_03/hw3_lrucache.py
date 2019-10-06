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
        if (isinstance(ttl, float)) or (isinstance(ttl, int)):
            self.ttl = ttl
        else:
            self.ttl = 10000000
        self.maxsize = maxsize

    def __call__(self, function):
        # TODO вызов функции
        cache = {}

        def wrapped(*args, **kwargs):
            args_hash = hash(tuple([args, frozenset(kwargs)]))
            if args_hash not in cache:
                if len(cache) == self.maxsize:
                    self.delete_lru_record(cache)
                cache[args_hash] = [function(*args, **kwargs),
                                    time.time() * 1000,
                                    time.time() * 1000]
            else:
                if time.time() * 1000 - cache[args_hash][1] > self.ttl:
                    cache[args_hash] = [function(*args, **kwargs),
                                        time.time() * 1000,
                                        time.time() * 1000]
                else:
                    cache[args_hash][2] = time.time() * 1000
            return cache[args_hash][0]
        return wrapped

    def delete_lru_record(self, cache):
        min_time = time.time() * 1000
        min_key = 0
        for key, value in cache.items():
            if value[2] < min_time:
                min_time = value[2]
                min_key = key
        del cache[min_key]
