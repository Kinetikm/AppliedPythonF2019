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
        self.time_dict = {}
        self.hash_table = {}
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        # raise NotImplementedError

    def __call__(self, function):  # *args, **kwargs
        # TODO вызов функции

        def wrapped(*args, **kwargs):
            cur_time = round(time.time() * 1000)

            if args in self.hash_table:
                if False if self.ttl is None else \
                        (cur_time - self.time_dict[args]) > self.ttl:
                    self.time_dict.pop(args)
                    self.hash_table.pop(args)

            if args in self.hash_table:
                self.time_dict[args] = cur_time
                return self.hash_table[args]

            result = function(*args, **kwargs)

            if len(self.hash_table) == self.maxsize:
                oldest_key = self._get_max_time()
                self.hash_table.pop(oldest_key)
                self.time_dict.pop(oldest_key)

            self.hash_table[args] = result
            self.time_dict[args] = round(time.time() * 1000)

            return result

        return wrapped

    def _get_max_time(self):
        min_born = round(time.time() * 1000)
        old_key = None
        for key, born in self.time_dict.items():
            if min_born >= born:
                min_born = born
                old_key = key
        return old_key
