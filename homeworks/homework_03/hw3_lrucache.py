#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:

    __slots__ = ["maxsize", "ttl", "cache", "record_time"]

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl

        self.cache = dict()
        self.record_time = dict()

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            cur_time = time()

            packet = tuple((args, str(kwargs)))

            if packet in self.cache:
                if self.ttl is not None:
                    if (cur_time - self.record_time[packet]) < self.ttl:
                        self.record_time[packet] = cur_time

                        return self.cache[packet]
                    else:
                        result = func(*args, **kwargs)

                        self.cache[packet] = result
                        self.record_time[packet] = cur_time
                else:
                    self.record_time[packet] = cur_time

                    return self.cache[packet]
            else:
                while len(self.cache) >= self.maxsize:
                    key_packet = min(self.record_time, key=lambda unit: self.record_time[unit])

                    del self.record_time[key_packet]
                    del self.cache[key_packet]

                result = func(*args, **kwargs)

                self.cache[packet] = result
                self.record_time[packet] = cur_time

            return result

        return wrapper
