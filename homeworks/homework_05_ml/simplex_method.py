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

    a = a.astype(dtype=float)
    b = b.astype(dtype=float)
    c = -c.astype(dtype=float)

    n, m = a.shape

    simplex_table = np.append(a, [c], axis=0)
    simplex_table = np.append(simplex_table, np.eye(n + 1), axis=1)
    b_column = np.append(b, [0], axis=0).reshape(n + 1, 1)
    simplex_table = np.append(simplex_table, b_column, axis=1)

    while min(simplex_table[-1, :]) < 0:
        indices_pivot_column = np.argmin(simplex_table[-1, :], axis=0)

        indices_pivot_row = np.argmin(simplex_table[:, -1][:-1] / simplex_table[:, indices_pivot_column][:-1])

        simplex_table[indices_pivot_row, :] /= simplex_table[indices_pivot_row, indices_pivot_column]
        for i in range(n + 1):
            if i != indices_pivot_row:
                simplex_table[i, :] -= simplex_table[indices_pivot_row, :] * simplex_table[i, indices_pivot_column]

        result = np.array([])
        for i in range(m):
            if len(np.nonzero(simplex_table[:, i])[0]) == 1:
                indices_first_non_zero = np.nonzero(simplex_table[:, i])[0]
                result = np.append(result, simplex_table[indices_first_non_zero, -1])
            else:
                result = np.append(result, [0])

    return result
