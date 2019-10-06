#!/usr/bin/env python
# coding: utf-8


import time
import operator


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        if ttl is not None:
            self.ttl = int(ttl)
        else:
            self.ttl = None
        self.cash = {}

    def __call__(self, function):
        def wrapped(*args, **kwargs):
            if (args in self.cash) and (self.ttl is not None) and \
             (abs(time.time() - self.cash.get(args)[1]) > self.ttl):
                self.cash.pop(args)
            if args in self.cash:
                time.sleep(0.00001)
                cur_time = time.time()
                self.cash.get(args)[1] = cur_time
                return self.cash.get(args)[0]
            if len(self.cash) == self.maxsize:
                old = (min(self.cash.items(), key=operator.itemgetter(1))[0])
                self.cash.pop(old)
            result = function(*args, **kwargs)
            self.cash[args] = []
            self.cash.get(args).append(result)
            cur_time = time.time()
            self.cash.get(args).append(cur_time)
            return result
        return wrapped
