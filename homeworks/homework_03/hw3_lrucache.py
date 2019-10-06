#!/usr/bin/env python
# coding: utf-8
import time
import operator


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        self.maxsize = maxsize
        if ttl is not None:
            self.ttl = int(ttl)
        else:
            self.ttl = None
        self.cash = {}

    def __call__(self, fn):
        def decorated(*args, **kwargs):
            if args in self.cash:
                if self.ttl:
                    if (abs(time.time() - self.cash.get(args)[1]) >
                            self.ttl):
                        self.cash.pop(args)
            if args in self.cash:
                time.sleep(0.00001)
                time_return_call = time.time()
                self.cash.get(args)[1] = time_return_call
                return self.cash.get(args)[0]
            if len(self.cash) == self.maxsize:
                help_dict = {}
                for _ in self.cash:
                    help_dict[_] = self.cash.get(_)[1]
                old = (min(help_dict.items(), key=operator.itemgetter(1))[0])
                self.cash.pop(old)
            result = fn(*args, **kwargs)
            self.cash[args] = []
            self.cash.get(args).append(result)
            time_first_call = time.time()
            self.cash.get(args).append(time_first_call)
            return result
        return decorated
