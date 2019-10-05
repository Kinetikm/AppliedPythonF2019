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
            key += kwd_mark
            for item in kwds.items():
                key += item
        return key

    def __call__(self, func):
        def cache(*args, **kwargs):
            key = self._make_key(args, kwargs)
            if key in self._results_dict:
                if self._max_time is not None and time.time() - self._times_dict[key] < self._max_time:
                    self._times_dict[key] = time.time()
                    return self._results_dict[key]
                elif self._max_time is None:
                    self._times_dict[key] = time.time()
                    return self._results_dict[key]
            res = func(*args, **kwargs)
            if self._current_size == self._maxsize:
                del_key = min(self._times_dict, key=self._times_dict.get)
                del self._results_dict[del_key]
                del self._times_dict[del_key]
                self._current_size -= 1
            self._times_dict[key] = time.time()
            self._results_dict[key] = res
            self._current_size += 1
            return res
        return cache


if __name__ == '__main__':
    @LRUCacheDecorator(maxsize=3, ttl=None)
    def get_sq(s):
        time.sleep(2)
        return s ** 2

    get_sq(1)
    get_sq(2)
    get_sq(3)
    get_sq(1)
    get_sq(4)
    get_sq(5)

    t_start = time.time()
    get_sq(1)
    assert time.time() - t_start < 0.5
