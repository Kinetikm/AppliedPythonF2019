#!/usr/bin/env python
# coding: utf-8

from time import time
from collections import Hashable


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.__cache = dict()

    def __get_hash(self, arg):
        if isinstance(arg, Hashable):
            return hash(arg)
        return hash(tuple(arg))

    def __get_full_hash(self, *args, **kwargs):
        hash = str()
        for arg in args:
            hash += str(self.__get_hash(arg))
        for key in kwargs:
            hash += str(self.__get_hash(kwargs[key]))
        return hash

    def __call__(self, func):
        def caccess(*args, **kwargs):
            hash = self.__get_full_hash(*args, **kwargs)
            if hash in self.__cache:
                # Если в кеше
                if (self.ttl is not None and
                   (time() - self.__cache[hash][0]) * 1000 > self.ttl):
                    # Если в кеше, но не валиден
                    self.__cache[hash][1] = func(*args, **kwargs)
                    self.__cache[hash][0] = time()
                    self.__cache[hash][2] = self.__cache[hash][0]
                    return self.__cache[hash][1]
                else:
                    # Если в кеше и валиден
                    self.__cache[hash][2] = time()
                    return self.__cache[hash][1]

            while len(self.__cache) >= self.maxsize:
                # Если не в кеше, в кеше нет места
                time_min = time()
                key_min = None
                for key in self.__cache:
                    if self.__cache[key][2] <= time_min:
                        time_min = self.__cache[key][2]
                        key_min = key
                self.__cache.pop(key_min)

            fret = func(*args, **kwargs)
            ctime = time()
            self.__cache.update({hash: [ctime, fret, ctime]})
            return fret
        return caccess
