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
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.has_func = False

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        if not self.has_func:
            self.func = args[0]
            self.has_func = True
            return self
        parameters = (args, tuple(kwargs.items()))
        if parameters in self.cache:
            cur_time = time.time()
            if self.ttl is not None:
                if cur_time - self.cache[parameters][1] < self.ttl:
                    res = self.cache[parameters][0]
                    self.cache[parameters] = res, cur_time
                    return res
                res = self.func(*args, **kwargs)
                self.cache[parameters] = res, cur_time
                return res
            res = self.cache[parameters][0]
            self.cache[parameters] = res, cur_time
            return res
        elif len(self.cache) != self.maxsize:
            cur_time = time.time()
            res = self.func(*args, **kwargs)
            self.cache[parameters] = res, cur_time
            return res
        else:
            if self.ttl is not None:
                old_keys = [k for k, v in self.cache.items() if time.time() - v[1] >= self.ttl]
                for key in old_keys:
                    del self.cache[key]
                if len(self.cache) != self.maxsize:
                    cur_time = time.time()
                    res = self.func(*args, **kwargs)
                    self.cache[parameters] = res, cur_time
                    return res
            sorted_cache = sorted(self.cache.items(), key=lambda t: -t[1][1])
            last_key, last_val = sorted_cache[-1]
            del self.cache[last_key]
            cur_time = time.time()
            res = self.func(*args, **kwargs)
            self.cache[parameters] = res, cur_time
            return res
