#!/usr/bin/env python
# coding: utf-8


import time


class LRUCacheDecorator:
    class LRUCacheItem:
        """Data structure of items stored in cache"""

        def __init__(self, args, key):
            self.args_str = str(args)
            self.key = key
            self.cached_result = None
            self.timestamp = time.time()

        def __str__(self):
            return self.args_str

        def __repr__(self):
            return self.args_str + ", time=" + str(self.timestamp)

        def __hash__(self):
            return self.key

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.key == other.key

        def set_cached_result(self, result):
            self.cached_result = result
            self.timestamp = time.time()

        def get_cached_result(self):
            return self.cached_result

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
        self.items = {}

    def __call__(self, *args, **kwargs):

        func = args[0]

        def decorator(*args, **kwargs):
            key = hash(str(args))
            if key in self.items:
                item = self.items[key]
                if not self.ttl_is_valid(item):
                    item.set_cached_result(func(*args, **kwargs))
                return item.get_cached_result()
            else:
                if len(self.items) + 1 > self.maxsize:
                    self.validate_cache()
                item = self.LRUCacheItem(args, key)
                item.set_cached_result(func(*args, **kwargs))
                self.items[key] = item
                return item.cached_result

        return decorator

    def remove_item(self, item):
        del self.items[item.key]

    def validate_cache(self):
        if self.ttl:
            for item in self.items.values():
                if not self.ttl_is_valid(item):
                    self.remove_item(item)
        else:
            self.items.popitem()

    def ttl_is_valid(self, item):
        if self.ttl:
            now = time.time()
            time_delta = now - item.timestamp
            return time_delta <= self.ttl
        else:
            return True
