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
    n = a.shape[0]
    len_x = a.shape[1]
    simp_table = np.vstack((a, -1 * c))
    simp_table = np.hstack((simp_table, np.eye(n + 1)))
    b = np.append(b, [0])
    b = b.reshape((n + 1, 1))
    simp_table = np.hstack((simp_table, b))
    n = simp_table.shape[0] - 1
    m = simp_table.shape[1] - 1
    y_j = np.arange(m)
    x_i = y_j[len_x:-1:]
    ans = np.zeros((len_x,))
    while simp_table[n, 0:m].min() < 0:
        j = simp_table[n].argmin()
        i = (simp_table[0:n, m] / simp_table[0:n, j]).argmin()
        y_j[j], x_i[i] = x_i[i], y_j[j]
        simp_table[i] /= simp_table[i, j]
        for iter in range(n + 1):
            if iter != i:
                simp_table[iter] -= simp_table[iter, j] * simp_table[i]
    for i in range(len(x_i)):
        if x_i[i] < len_x:
            ans[x_i[i]] = simp_table[i, m]
    return ans
