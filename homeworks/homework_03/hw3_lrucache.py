#!/usr/bin/env python
# coding: utf-8
import time
from functools import wraps


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
        self.cache = []
        self.arguments = []
        self.timeQueue = []

    def __call__(self, func):
        # TODO вызов функции

        @wraps(func)
        def wrapped(*args, **kwargs):
            tm = time.time()
            temp = [args, kwargs]
            if (temp in self.arguments) and (
                    not bool(self.time) or (tm - self.timeQueue[self.arguments.index(temp)] < self.time / 1000)):
                pos = self.arguments.index(temp)
                result = self.cache.pop(pos)
                self.timeQueue.pop(pos)
                self.arguments.pop(pos)
                self.arguments.append(temp)
                self.cache.append(result)
                self.timeQueue.append(tm)
                return result
            if temp in self.arguments:
                pos = self.arguments.index(temp)
                self.cache.pop(pos)
                self.timeQueue.pop(pos)
                self.arguments.pop(pos)
            result = func(*args, **kwargs)
            if len(self.arguments) >= self.max:
                self.cache.pop(0)
                self.timeQueue.pop(0)
                self.arguments.pop(0)
            self.arguments.append(temp)
            self.cache.append(result)
            tm = time.time()
            self.timeQueue.append(tm)
            return result
        return wrapped
