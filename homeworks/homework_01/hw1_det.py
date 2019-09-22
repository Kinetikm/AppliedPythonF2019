#!/usr/bin/env python
# coding: utf-8
import copy


def minor(M0, i, j):
    M = copy.deepcopy(M0)#чтобы не менять основу
    del M[i]
    for i in range(len(M0[0]) - 1):
        del M[i][j]#убираем столбец
    return M


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    if not list_of_lists:
        return None

    r = len(list_of_lists[0])

    if len(list_of_lists) != r:
        return None
    if r == 1:
        return list_of_lists[0][0]

    sign = 1
    det = 0
    # разложение по первой строке
    for j in range(r):
        det += list_of_lists[0][j] * sign * calculate_determinant(minor(list_of_lists, 0, j))
        sign *= -1

    return det
