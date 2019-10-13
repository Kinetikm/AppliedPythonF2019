#!/usr/bin/env python
# coding: utf-8
from time import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.time_dict = OrderedDict()  # поменял обычный словарь на OrderedDict так как в нем все значения будут
        self.cache = dict()  # лежать по дате добавления, то есть не придется тратить время на поиск самого
        # старого значения

    def __call__(self, func):
        @wraps(func)
        def lrucache(*args, **kwargs):
            key = ((args, str(kwargs)))
            if key not in self.cache:  # если значения нет в кэше, вычислим его
                result = func(*args, **kwargs)
                if self.maxsize > len(self.cache):  # если размерность кэша меньше ограничения,
                    self.time_dict[key] = time()  # то забиваем новое значение и сохраняем время
                    self.cache[key] = result
                else:  # если больше ограничения
                    item = self.time_dict.popitem()  # то берем самое старое значение и удаляем его
                    item = item[0]
                    self.cache.pop(item)
                    self.time_dict[key] = time()  # забиваем новое значение и сохраняем время
                    self.cache[key] = result
            else:  # если время хранения значения больше положенного, то вычисляем заново
                if self.ttl is not None and (time() - self.time_dict[key]) * 1000 > self.ttl:
                    result = func(*args, **kwargs)
                    self.time_dict[key] = time()
                    self.cache[key] = result
                else:  # а если с временем все ок, то просто вернем значение
                    result = self.cache[key]
            return result

        return lrucache
