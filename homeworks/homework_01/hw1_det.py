#!/usr/bin/env python
# coding: utf-8

def det(list_of_lists, l, deleted):
    if l == len(list_of_lists) - 1:
        for i in range(len(list_of_lists)):
            if deleted[i] == 0:
                return list_of_lists[i][l]
    d = 0
    k = 1
    for i in range(len(list_of_lists)):
        if deleted[i] == 0:
            deleted[i] = 1
            d += k * list_of_lists[i][l] * det(list_of_lists, l + 1, deleted)
            k *= -1
            deleted[i] = 0
    return d
def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    if len(list_of_lists) == 0:
        return None
    deleted = [0] * len(list_of_lists)
    for i in range(len(list_of_lists)):
        if len(list_of_lists) != len(list_of_lists[0]):
            return None
    return det(list_of_lists, 0, deleted)
