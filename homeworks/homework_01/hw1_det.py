#!/usr/bin/env python
# coding: utf-8


def minor(A, i, j):
    m = [row[:] for row in A]
    del m[i]
    for k in range(len(A[0]) - 1):
        del m[k][j]
    return m


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    a = list_of_lists
    m = len(a)
    n = len(a[0])

    if m == 0 or n != m or n == 0:
        return None
    if m == 1:
        return a[0][0]

    if m == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    # по первому столбцу
    sign = 1
    det = 0

    for i in range(m):
        det = det + a[i][0] * sign * calculate_determinant(minor(a, i, 0))
        sign = (-1) * sign

    return det
