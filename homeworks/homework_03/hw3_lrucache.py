#!/usr/bin/env python
# coding: utf-8
import time
from collections import OrderedDict


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        self.ttl = ttl
        self.size = maxsize
        self.dict = OrderedDict()  # {num: (add time, num**2)}
        self.f = None

    def __call__(self, *args, **kwargs):
        if not self.f:
            self.f = args[0]
            return self

        if args[0] in self.dict:
            item = self.dict[args[0]]
            self.dict.move_to_end(args[0])
            if self.ttl and time.time() - item[0] > self.ttl:
                res = self.f(args[0])
                self.dict[args[0]] = tuple((time.time(), res))
                return res
            else:
                return item[1]
        else:
            if len(self.dict) >= self.size:
                self.dict.popitem(last=False)
            res = self.f(args[0])
            self.dict[args[0]] = tuple((time.time(), res))
            self.dict.move_to_end(args[0])
            return res


@LRUCacheDecorator(maxsize=3, ttl=1)
def get_sq(s):
    time.sleep(2)
    return s ** 2
