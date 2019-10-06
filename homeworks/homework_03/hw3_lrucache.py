#!/usr/bin/env python
# coding: utf-8


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        # TODO вызов функции
        raise NotImplementedError
