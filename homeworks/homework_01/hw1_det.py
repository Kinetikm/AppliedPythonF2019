#!/usr/bin/env python
# coding: utf-8
import copy


def f(list_of_lists, i, j):
    newList = copy.deepcopy(list_of_lists)
    del newList[i]
    while i < len(list_of_lists[0]) - 1:
        del newList[i][j]
        i += 1
    return newList


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    i = 0
    while i < len(list_of_lists):
        if len(list_of_lists) != len(list_of_lists[i]):
            return None
        i += 1
    if len(list_of_lists[0]) == 1:
        return list_of_lists[0][0]
    i = 0
    sign = 1
    det = 0
    while i < len(list_of_lists):
        det += list_of_lists[0][i] * sign * calculate_determinant(f(list_of_lists, 0, i))
        sign = sign * (-1)
        i += 1
    return det
