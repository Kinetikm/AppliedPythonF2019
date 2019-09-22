#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''

    det = 0
    new_list = []
    for i in range(len(list_of_lists)):
        if len(list_of_lists[i]) != len(list_of_lists):
            return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    for i in range(len(list_of_lists)):
        new_list = [a[:] for a in list_of_lists]
        det += list_of_lists[0][i] * (-1) ** (i) * ad(new_list[1:], i)
    return det


def ad(listik, k):
    detik = 0
    for j in range(len(listik)):
        del listik[j][k]
    if (len(listik) == 1):
        return listik[0][0]
    else:
        for i in range(len(listik)):
            new_list1 = [a[:] for a in listik]
            detik += listik[0][i] * (-1) ** (i) * ad(new_list1[1:], i)
        return detik
