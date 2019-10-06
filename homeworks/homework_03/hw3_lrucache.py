#!/usr/bin/env python
# coding: utf-8


import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache_dict = {}    # key: args, value: time

    def __call__(self, func):
        def decor(*args, **kwargs):
            if str([args, kwargs]) not in self.cache_dict:
                if len(self.cache_dict) == self.maxsize:
                    oldest = time.time()
                    for value in self.cache_dict.values():
                        if oldest > value[0]:
                            oldest = value[0]
                    for key in self.cache_dict:
                        if self.cache_dict[key][0] == oldest:
                            print("must del {}".format(key))
                            del self.cache_dict[key]
                            break
                result = func(*args, **kwargs)
                self.cache_dict[str([args, kwargs])] = (time.time(), result)
                print()
                return result
            else:
                if self.ttl is not None:
                    print(self.cache_dict[str([args, kwargs])][0] - time.time())
                    if (- self.cache_dict[str([args, kwargs])][0] + time.time()) * 1000 > self.ttl:
                        del self.cache_dict[str([args, kwargs])]
                        self.cache_dict[str([args, kwargs])] = (time.time(), func(*args, **kwargs))
                    else:
                        self.cache_dict[str([args, kwargs])] = (time.time(), self.cache_dict[str([args, kwargs])][1])
                else:
                    self.cache_dict[str([args, kwargs])] = (time.time(), self.cache_dict[str([args, kwargs])][1])
                return self.cache_dict[str([args, kwargs])][1]
        return decor
