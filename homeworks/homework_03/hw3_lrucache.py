#!/usr/bin/env python
# coding: utf-8
from time import time
import functools
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl

        self.cached = OrderedDict()
        self.results_times = OrderedDict()

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cur_time = time()

            packet = tuple((args, str(kwargs)))

            if packet in self.cached:
                if self.ttl is not None:
                    if (cur_time - self.results_times[packet]) < self.ttl:
                        self.results_times[packet] = cur_time

                        return self.cached[packet]
                    else:
                        result = func(*args, **kwargs)
                        self.cached[packet] = result
                        self.results_times[packet] = cur_time
                else:
                    self.results_times[packet] = cur_time

                    return self.cached[packet]
            else:
                if len(self.cached) >= self.maxsize:
                    self.results_times.popitem()  # c last=False не проходит тесты
                    self.cached.popitem()

                result = func(*args, **kwargs)
                self.cached[packet] = result
                self.results_times[packet] = cur_time

            return result

        return wrapper
