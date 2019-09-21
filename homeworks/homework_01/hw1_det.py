#!/usr/bin/env python
# coding: utf-8

from copy import deepcopy


def minor(mtrx, i, j):
    minore = deepcopy(mtrx)
    del minore[i]
    for i in range(len(mtrx) - 1):
        del minore[i][j]
    return minore


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''

    mtrx = list_of_lists
    n = len(mtrx)
    sgn = 1
    det = 0
    if n != len(mtrx[0]):
        return None
    elif n == 1:
        return mtrx[0][0]
    else:
        for i in range(n):
            det += mtrx[0][i] * sgn * calculate_determinant(minor(mtrx, 0, i))
            sgn *= -1
        return det
