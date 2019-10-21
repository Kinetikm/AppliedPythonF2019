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
    matr = np.vstack([a, (-1) * c])
    matr = np.hstack([matr, np.append(b, 0).reshape([matr.shape[0], 1])])
    elem_mask = [-1 for _ in range(a.shape[0])]
    while not all([matr[-1][i] >= 0 for i in range(len(matr[-1]))]):
        min_el = min(matr[-1])
        min_num_col = np.where(matr[-1] == min_el)[0][0]
        b_div = matr[:-1, -1] / matr[:-1, min_num_col]
        min_el = min(b_div)
        min_num_row = np.where(b_div == min_el)[0][0]
        new_row = matr[min_num_row] / matr[min_num_row, min_num_col]
        tmp_matr = np.delete(matr, min_num_row, axis=0)
        elem_mask[min_num_row] = min_num_col
        new_matr = np.zeros(tmp_matr.shape)
        for numr, row in enumerate(tmp_matr):
            tmp_row = new_row * row[min_num_col]
            new_matr[numr] = (row - tmp_row).copy()
        matr = np.vstack([new_matr[:min_num_row], new_row, new_matr[min_num_row:]])
    x = np.zeros(c.shape)
    for num, i in enumerate(elem_mask):
        if i > -1:
            x[i] = matr[:, -1][num]
    return x
