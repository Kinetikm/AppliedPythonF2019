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
        self._maxsize = maxsize
        self._ttl = ttl
        self._cach = {}
        self._times = {}

    def __call__(self, func):
        def cach(*args, **kwargs):
            args = ((args, str(kwargs)))
            if args in self._cach:
                if self._ttl and (time() - self._times[args])*1000 > self._ttl:
                    result = func(*args, **kwargs)
                    self._cach[args] = result
                    self._time[args] = time()
                else:
                    result = self._cach[args]
                    self._time[args] = time()
            else:
                result = func(*args, **kwargs)
                if len(self._cach) >= self._maxsize:
                    self._pop()
                self._cach[args] = result
                self._time[args] = time()

    def _pop(self):
        oldness = time()
        for args in self._cach.keys():
            tmp_time = self._time[args]
            if tmp_time < oldness:
                oldness = tmp_time
                pop_args = args
        self._cach.pop(pop_args)
        self._time.pop(pop_args)
        
                
