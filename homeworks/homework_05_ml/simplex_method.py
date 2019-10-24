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
    def table_build(a, b, c):
        b = b.reshape(a.shape[0], 1)
        c = c.reshape(1, a.shape[1])
        c = np.hstack((c, np.zeros((1, a.shape[0]))))
        a = np.hstack((a, np.eye(a.shape[0])))
        add_bottom = np.vstack((a, np.negative(c)))
        b = np.append(b, 0)
        table = np.column_stack((add_bottom, b))
        return table.astype(float)

    def next_round(table):
        m = min(table[-1, :-1])
        if m >= 0:
            return False
        else:
            return True

    def pivot(table, slack):
        neg_index = np.argmin(table[-1, :-1])
        piv_row = np.argmin(table[:-1, -1] / table[:-1, neg_index])
        table[piv_row] = table[piv_row]/table[piv_row, neg_index]
        slack[piv_row] = neg_index
        for i in range(table.shape[0]):
            if i == piv_row:
                table[i] -= table[piv_row]*(table[i, neg_index]/table[piv_row, neg_index])
        return table
    slack = [-1 for i in range(a.shape[0])]
    x = np.zeros(a.shape[1])
    table = table_build(a, b, c)
    while(next_round(table)):
        table = pivot(table, slack)
    for i in range(a.shape[0]):
        if slack[i] != -1:
            x[slack[i]] = table[i, -1]
    return x
