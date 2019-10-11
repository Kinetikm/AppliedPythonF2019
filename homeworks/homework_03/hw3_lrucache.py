#!/usr/bin/env python
# coding: utf-8
import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        # инициализация декоратора
        #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        self._maxsize = maxsize
        self._current_size = 0
        self._results_dict = {}
        self._times_dict = {}
        self._max_time = ttl
        if self._max_time is not None:
            self._max_time /= 1000  # time in second

    def _make_key(self, args, kwds, kwd_mark=(object(),)):
        key = args
        if kwds:
            key += kwd_mark  # добавляем разделитель между args и kwargs, чтобы для вызовы
            # decorated_func(1, 2, 3, 'a', 'x')  decorated_func(1, 2, 3, a='x') получались разные ключи
            for item in kwds.items():
                key += item
        return key

    def __call__(self, func):
        def cache(*args, **kwargs):
            key = self._make_key(args, kwargs)
            if key in self._results_dict:
                if self._max_time is None or time.time() - self._times_dict[key] < self._max_time:
                    # в кэше есть достаточно свежий элемент, либо нас устраивает элемент любой давности
                    # times_dict упорядочен по времени обращения к функции, поэтому заменяем элемент,
                    #  к которому обращаемся чтобы он был в конце
                    del self._times_dict[key]
                    self._times_dict[key] = time.time()
                    return self._results_dict[key]
            # в кэше нужного элемента нет, либо он слишком старый
            res = func(*args, **kwargs)
            if self._current_size == self._maxsize:
                # размер кэша достиг максимального, поэтому выкидываем самый старый элемент (первый)
                del_key = next(iter(self._times_dict.keys()))
                del self._results_dict[del_key]
                del self._times_dict[del_key]
                self._current_size -= 1
            # теперь добавим в кэш полученный резултат
            self._times_dict[key] = time.time()
            self._results_dict[key] = res
            self._current_size += 1
            return res
        return cache
