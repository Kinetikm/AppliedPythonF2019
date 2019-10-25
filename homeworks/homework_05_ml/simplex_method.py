#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://  https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    def _create_table(a, b, c):
        pivot = np.vstack((a, c * (-1)))
        pivot = np.hstack((pivot, np.eye(pivot.shape[0])))
        pivot = np.hstack((pivot, np.append(b, 0).reshape(-1, 1)))
        return pivot

    def _has_negative(_table):
        for i in _table[-1]:
            if i < 0:
                return True
        return False

    def _pivotize(x, y, _table):
        _table[y] = _table[y] / _table[y][x]
        for i in range(_table.shape[0]):
            if i != y:
                _table[i] = _table[i] - _table[y] * _table[i][x]

    table = _create_table(a, b, c)
    result_ids = np.full(a.shape[0], -1)
    while _has_negative(table):
        x = table[-1][:-1].argmin()
        y = (table[:, -1] / table[:, x])[:-1].argmin()
        result_ids[y] = x
        _pivotize(x, y, table)
    result = np.zeros(c.shape[0])
    for i in range(a.shape[0]):
        if result_ids[i] != -1:
            result[result_ids[i]] = table[:, -1][i]
    return result
