#!/usr/bin/env python
# coding: utf-8

import copy


def minor(mtrx, i, j):
    A = copy.deepcopy(mtrx)
    del A[i]
    for i in range(len(mtrx[0]) - 1):
        del A[i][j]
    return A


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    m = len(list_of_lists)
    n = len(list_of_lists[0])

    if m != n:
        return
    elif m == 1:
        return list_of_lists[0][0]

    sign = 1

    result = 0

    for j in range(n):
        result += list_of_lists[0][j] * sign * calculate_determinant(minor(list_of_lists, 0, j))
        sign *= -1

    return result
