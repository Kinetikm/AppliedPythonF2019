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
    x = np.zeros((1, a.shape[1]))
    # Create a table
    b = b.reshape(-1, 1)
    b = np.vstack((b, np.zeros((1, 1))))
    table = np.vstack((a, -c))
    table = np.hstack((table, np.eye(table.shape[0])))
    table = np.hstack((table, b))
    while not (table[-1, :] >= 0).prod():
        idx_col = table[-1, :].argmin()
        idx_row = (table[:-1, -1] / table[:-1, idx_col]).reshape(-1, 1).argmin()
        table[idx_row, :] = table[idx_row, :] / table[idx_row, idx_col]
        for row in range(table.shape[0]):
            if row != idx_row:
                table[row, :] += table[idx_row, :] * (-table[row, idx_col])
    for row in range(table.shape[0] - 1):
        for col in range(a.shape[1]):
            if table[row, col] == 1.0:
                x[0, col] = table[row, -1]
    return x.reshape(-1,)
