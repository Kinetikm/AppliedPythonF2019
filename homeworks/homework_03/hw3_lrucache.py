#!/usr/bin/env python
# coding: utf-8


from time import time
from functools import wraps
from collections import deque


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        if ttl:
            self.ttl = ttl / 1000
        else:
            self.ttl = None
        self.cache = {}
        #self.cache_time = {}
        self.key_time_queue = deque()

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key not in self.cache:
                if len(self.cache) == self.maxsize:
                    del_key = self.key_time_queue.popleft()
                    del self.cache[del_key]
                    #del self.cache_time[del_key]
                self.cache[key] = [func(*args, **kwargs), time()]
                #self.cache_time[key] = time()
                self.key_time_queue.append(key)
                return self.cache[key][0]
            else:
                if self.ttl and (time() - self.cache[key][1]) > self.ttl:
                    #self.cache_time[key] = time()
                    self.cache[key] = [func(*args, **kwargs), time()]
                    self.key_time_queue.remove(key)
                    self.key_time_queue.append(key)
                else:
                    self.cache[key][1] = time()
                    self.key_time_queue.remove(key)
                    self.key_time_queue.append(key)
                return self.cache[key][0]
        return inner
