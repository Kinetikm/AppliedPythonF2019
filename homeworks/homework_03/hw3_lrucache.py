#!/usr/bin/env python
# coding: utf-8
import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.max = maxsize
        self.time = ttl
        self.cache = dict()
        self.timeQueue = OrderedDict()  # для того, чтобы всё было в нужном порядке не теряя скорости

    def __call__(self, func):
        # TODO вызов функции

        @wraps(func)
        def wrapped(*args, **kwargs):
            temp = str(args)+str(kwargs)  # чтобы было хэшируемо
            if (temp in self.cache) and (
                    not bool(self.time) or (time.time() - self.timeQueue[temp] < self.time / 1000)):
                result = self.cache[temp]
                self.timeQueue[temp] = time.time()
                self.timeQueue.move_to_end(temp, False)
                return result
            if temp in self.cache:
                self.cache.pop(temp)
                self.timeQueue.pop(temp)
            result = func(*args, **kwargs)
            if len(self.cache) >= self.max:
                key = self.timeQueue.popitem()
                key = key[0]
                self.cache.pop(key)
            self.cache[temp] = result
            tm = time.time()
            self.timeQueue[temp] = time.time()
            self.timeQueue.move_to_end(temp, False)
            return result
        return wrapped
