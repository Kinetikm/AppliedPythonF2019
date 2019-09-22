#!/usr/bin/env python
# coding: utf-8
import copy

def minor(M, i, j):
    copy_M = copy.deepcopy(M)
    del copy_M[i]
    for i in range(len(M[0]) - 1):
        del copy_M[i][j]
    return copy_M


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''

    n = len(list_of_lists[0])

    if len(list_of_lists) != n:
        return None
    if n == 1:
        return list_of_lists[0][0]

    k = 1
    det = 0
    for j in range(n):
        det += list_of_lists[0][j] * k * calculate_determinant(minor(list_of_lists, 0, j))
        k *= -1
    return det
