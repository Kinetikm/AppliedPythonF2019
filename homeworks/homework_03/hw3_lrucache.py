#!/usr/bin/env python
# coding: utf-8

import functools
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self._maxsize = maxsize
        self._ttl = ttl
        self._mem = {}

    def __call__(self, *args, **kwargs):
        self._func = args[0]

        @functools.wraps(self._func)
        def wrapper(*args, **kwargs):
            key = "".join(map(str, (args, sorted(kwargs))))
            if key not in self._mem:
                if len(self._mem) + 1 > self._maxsize:
                    del self._mem[self.del_old()]
                self._mem[key] = (time.time(), self._func(*args, **kwargs))
            elif self._ttl is not None:
                if time.time() - self._mem[key][0] > self._ttl:
                    self._mem[key] = (time.time(), self._func(*args, **kwargs))
            return self._mem[key][1]
        return wrapper

    def del_old(self):
        self._maxtime = time.time()
        self._now = time.time()
        for item in self._mem.items():
            self._tm = self._now - item[1][0]
            if self._tm < self._maxtime:
                self._maxtime = self._tm
                self._key = item[0]
        return self._key
