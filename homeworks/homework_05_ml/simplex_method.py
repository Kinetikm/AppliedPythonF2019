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
    n, m = a.shape
    col_labels = np.array(range(n + m + 1))
    row_labels = np.array([m + i for i in range(n)])
    a = np.concatenate((a, c.reshape(1, m) * (-1)), axis=0)
    a = np.concatenate((a, np.eye(n + 1)), axis=1)
    b = np.vstack((b.reshape(n, 1), np.array([[0]])))
    a = np.hstack((a, b))
    pivot_col = np.argmin(a[-1, :-1])
    el = a[-1, pivot_col]
    while el < 0:
        pivot_row = np.argmin(a[:-1, -1] / a[:-1, pivot_col])
        row_labels[pivot_row], col_labels[pivot_col] = col_labels[pivot_col], row_labels[pivot_row]
        a[pivot_row] = a[pivot_row, :] / a[pivot_row, pivot_col]
        r = np.copy(a[pivot_row])
        a = a + (-a[:, pivot_col]).reshape(n+1, 1) * r.reshape(1, n + m + 1 + 1)
        a[pivot_row] = r
        pivot_col = np.argmin(a[-1, :-1])
        el = a[-1, pivot_col]
    x = np.zeros(m + n)
    np.put(x, row_labels, a[:-1, -1])
    return x[:m]
