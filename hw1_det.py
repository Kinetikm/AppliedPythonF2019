#!/usr/bin/env python
# coding: utf-8
import copy

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
    for i in list_of_lists:
        n = len(i)
        if m != n:
            return None
    if m == 1:
        return list_of_lists[0][0]
    n = len(list_of_lists)
    det = 0
    for i in range(n):
        clmn = copy.deepcopy(list_of_lists)
        del clmn[0]
        for j in range(m - 1):
            del clmn[j][i]
        det += ((-1)**(i)) * list_of_lists[0][i] * calculate_determinant(clmn)
    return det
    # raise NotImplementedError