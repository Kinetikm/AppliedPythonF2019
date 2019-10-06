#!/usr/bin/env python
# coding: utf-8
import time
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()
        self.foo = None

    def __call__(self, *args, **kwargs):
        if self.foo is None:
            self.foo = args[0]
            return self
        else:
            arg = args[0]
            if arg in self.cache and (self.ttl is None or time.time() - self.cache[arg][1] <= self.ttl):
                self.cache[arg][1] = time.time()
                self.cache.move_to_end(arg)
                return self.cache[arg][0]

            res = self.foo(*args, **kwargs)

            if len(self.cache) == self.maxsize:
                self.cache.popitem(last=False)
            self.cache[arg] = [res, time.time()]
            return res
