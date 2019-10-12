#!/usr/bin/env python
# coding: utf-8

import functools
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self._maxsize = maxsize
        self._ttl = ttl
        if self._ttl:
            self._ttl /= 1000
        self._mem = {}
        self._bl = self._ttl is not None

    def __call__(self, *args, **kwargs):
        self._func = args[0]

        @functools.wraps(self._func)
        def wrapper(*args, **kwargs):
            key = "".join(map(str, (args, sorted(kwargs))))
            if key not in self._mem:
                if len(self._mem) + 1 > self._maxsize:
                    del self._mem[list(self._mem.keys())[0]]
                self._mem[key] = (self._func(*args, **kwargs), time.time())
            else:
                if self._bl and time.time() - self._mem[key][1] > self._ttl:
                    self._mem[key] = (self._func(*args, **kwargs), time.time())
                else:
                    val = self._mem[key][0]
                    del self._mem[key]
                    self._mem[key] = (val, time.time())
            return self._mem[key][0]
        return wrapper
