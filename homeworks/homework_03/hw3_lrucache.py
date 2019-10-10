#!/usr/bin/env python
# coding: utf-8


import time

class LRUCacheDecorator:
    class LRUCacheItem:
        """Data structure of items stored in cache"""

        def __init__(self, args):
            self.args_str = str(args)
            self.key = hash(self.args_str)
            self.cached_result = None
            self.timestamp = time.time()

        def __str__(self):
            return self.args_str

        def __repr__(self):
            return self.args_str

        def __hash__(self):
            return self.key

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.key == other.key

        def set_cached_result(self, result):
            self.cached_result = result
            self.timestamp = time.time()

        def get_cached_result(self):
            self.timestamp = time.time()
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
        self.item_list = []

    def __call__(self, *args, **kwargs):

        func = args[0]

        def decorator(*args, **kwargs):
            item = self.LRUCacheItem(args)
            print(self.item_list)
            if item in self.item_list:
                item_index = self.item_list.index(item)
                item = self.item_list[item_index]
                if not self.ttl_is_valid(item):
                    item.set_cached_result(func(*args, **kwargs))
                return item.get_cached_result()
            else:
                if len(self.item_list) + 1 > self.maxsize:
                    self.validate_cache()
                item.set_cached_result(func(*args, **kwargs))
                self.item_list.insert(0, item)
                return item.cached_result

        return decorator

    def remove_item(self, item):
        del self.item_list[self.item_list.index(item)]

    def validate_cache(self):
        if self.ttl:
            for item in self.item_list:
                if not self.ttl_is_valid(item):
                    self.remove_item(item)
        else:
            # now = time.time()
            # max_delta = -1
            # remove_candidate = None
            # for item in self.item_list:
            #     if (now - item.timestamp) > max_delta:
            #         max_delta = now - item.timestamp
            #         remove_candidate = item
            # if remove_candidate:
            #     self.remove_item(remove_candidate)
            self.remove_item(self.item_list[0])

    def ttl_is_valid(self, item):
        if self.ttl:
            now = time.time()
            time_delta = now - item.timestamp
            return time_delta <= self.ttl
        else:
            return True
