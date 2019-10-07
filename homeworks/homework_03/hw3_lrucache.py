#!/usr/bin/env python
# coding: utf-8


import time

class LRUCacheDecorator:

    class LRUCacheItem():
        """Data structure of items stored in cache"""

        def __init__(self, key, item):
            self.key = key
            self.item = item
            self.timestamp = time.time()

        def __eq__(self,other):
            if isinstance(other, self.__class__):
                return self.key == other.key and self.item == other.item

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
        self.hash = {}
        self.item_list = []

    def __call__(self, *args, **kwargs):

        func = args[0]

        def decorator(*args, **kwargs):
            key = self._hashargs(args, kwargs)
            item = self.LRUCacheItem(key, func(*args, **kwargs))
            if item.key in self.hash:
                item_index = self.item_list.index(item)
                self.item_list[:] = self.item_list[:item_index] + self.item_list[item_index + 1:]
                self.item_list.insert(0, item)
            else:
                if len(self.item_list) > self.maxsize:
                    self.removeItem(self.item_list[-1])
            self.hash[item.key] = item
            self.item_list.insert(0, item)
            self.validateItem()
        return decorator

    def removeItem(self,item):
        del self.hash[item.key]
        del self.item_list[self.item_list.index(item)]

    def validateItem(self):
        if self.ttl:
            now = time.time()
            for item in self.item_list:
                time_delta = now - item.timestamp
                if time_delta > self.ttl:
                    self.removeItem(item)

    def _hashargs(self, args, kwargs):
        return hash(str(args) + str(kwargs))