#!/usr/bin/env python
# coding: utf-8

import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache_bank = dict()

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            cache = str(args) + str(kwargs)
            if cache in self.cache_bank.keys():
                if self.ttl:
                    if (time.time() - self.cache_bank[cache][1]) * 1000 < self.ttl:
                        return self.cache_bank[cache][0]
                    else:
                        if len(self.cache_bank.keys()) == self.maxsize:
                            del [self.cache_bank[min(self.cache_bank.items(), key=lambda x: x[1][1])[0]]]
                            res = f(*args, **kwargs)
                            self.cache_bank[cache] = [res, time.time()]
                            return res
                        else:
                            res = f(*args, **kwargs)
                            self.cache_bank[cache] = [res, time.time()]
                            return res
                else:
                    return self.cache_bank[cache][0]
            else:
                if len(self.cache_bank.keys()) == self.maxsize:
                    del[self.cache_bank[min(self.cache_bank.items(), key=lambda x: x[1][1])[0]]]
                    res = f(*args, **kwargs)
                    self.cache_bank[cache] = [res, time.time()]
                    return res
                else:
                    res = f(*args, **kwargs)
                    self.cache_bank[cache] = [res, time.time()]
                    return res
        return wrapped
