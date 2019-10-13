#!/usr/bin/env python
# coding: utf-8

import time
from functools import wraps
from collections import OrderedDict


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self.maxsize = maxsize
        self.ttl = ttl
        self.cashe = OrderedDict()  # {hash: [result fuc(), time of call], ...}

    def __call__(self, *args, **kwargs):
        # вызов функции
        func = args[0]

        @wraps(func)
        def inner(*args, **kwargs):
            h = hash(str(args) + str(kwargs))

            if h not in self.cashe:
                res = func(*args, **kwargs)
                if self.maxsize > len(self.cashe):  # если еще есть место
                    self.cashe[h] = [res, time.time()]
                else:  # если нет места, то удаляем самое старое значение (самое левое) и пишем новое
                    self.cashe.popitem(last=False)
                    self.cashe[h] = [res, time.time()]

            elif self.ttl is not None and (time.time() - self.cashe[h][1]) * 1000 > self.ttl:
                #  перезапишем значение, если последняя запись была давно
                res = func(*args, **kwargs)
                self.cashe[h] = [res, time.time()]
                self.cashe.move_to_end(h)

            else:
                self.cashe.move_to_end(h)
                return self.cashe[h][0]

            return res
        return inner
