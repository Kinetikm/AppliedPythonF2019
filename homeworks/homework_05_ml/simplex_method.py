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
    n, m = len(a), len(c)
    a = a.astype(np.float128)
    b = b.astype(np.float128)
    c = -1 * c.astype(np.float128)
    x = np.array([0.0 for _ in range(m)])
    dict_x = [i + m for i in range(n)]
    while True:
        row = c.argmin()
        if c[row] >= 0:
            break
        with np.errstate(divide='ignore'):
            column = (b / a[:, row]).argmin()
        dict_x[column] = row
        b[column] /= a[column][row]
        a[column] = a[column] / a[column][row]
        for i in range(n):
            if i == column:
                continue
            b[i] -= a[i][row] * b[column]
            a[i] -= a[i][row] * a[column]
        c -= c[row] * a[column]
    for i in range(n):
        if dict_x[i] >= m:
            continue
        x[dict_x[i]] = b[i]
    return x
