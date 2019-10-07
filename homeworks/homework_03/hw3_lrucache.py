#!/usr/bin/env python
# coding: utf-8
from time import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.time_dict = dict()
        self.cache = dict()

    def find_old_value(self, times, arg):
        mtime = -1
        item = -1
        if times > mtime:
            mtime = times
            item = arg
        return item

    def __call__(self, func):
        def lrucache(*args, **kwargs):
            key = ((args, str(kwargs)))
            item = 0
            if key not in self.cache:  # если значения нет в кэше, вычислим его
                result = func(*args, **kwargs)
                if self.maxsize > len(self.cache):  # если размерность кэша меньше ограничения,
                    self.time_dict[key] = time()  # то забиваем новое значение и сохраняем время
                    self.cache[key] = result
                else:  # если больше ограничения
                    for (arg, times) in self.time_dict.items():  # то ищем самое старое значение и удаляем его
                        item = self.find_old_value(times, arg)
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
