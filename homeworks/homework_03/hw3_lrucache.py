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
        self.time_lim = ttl
        self.cache = {}

    def __call__(self, func):

        def decor(*args, **kwargs):
            if self.time_lim is not None:  # Чищу от старых значений в кеше
                list_to_del = []
                for key, value in self.cache.items():
                    if time.time() * 1000 - value[1] > self.time_lim:
                        list_to_del.append(key)
                for key in list_to_del:
                    del self.cache[key]

            cache_key = hash(str(args)+str(kwargs))

            if cache_key not in self.cache:    # если от такого значения ещё не вычисляли
                result = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:      # если есть место
                    self.cache[cache_key] = [result, time.time()*1000]
                else:       # если места нет, то выбросим редкоиспользуемый
                    key_less = max(self.cache, key=lambda x: time.time()*1000 - self.cache[x][1])
                    del self.cache[key_less]
                    self.cache[cache_key] = [result, time.time()*1000]
                return result
            else:   # если значение вычислялось
                self.cache[cache_key][1] = time.time()*1000
                return self.cache[cache_key][0]
        return decor
