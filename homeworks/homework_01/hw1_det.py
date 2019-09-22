#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy as copy


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    n = len(list_of_lists)
    if n == 0 or n != len(list_of_lists[0]):
        return None
    if n == 1:
        return list_of_lists[0][0]
    if n == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
    mx = copy(list_of_lists)
    for i in range(n):
        for j in range(n - 1, i, -1):
            if mx[0][0]:
                k = mx[j][i] / mx[i][i]
            else:
                k = 0
            tmp = [k * a for a in mx[i]]
            # mx[j] = [b - a for a, b in (tmp, mx[j])]
            mx[j] = [mx[j][a] - tmp[a] for a in range(n)]
    d = 1
    for i in range(n):
        d *= mx[i][i]
    return d
