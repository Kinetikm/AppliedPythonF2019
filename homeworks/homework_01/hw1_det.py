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
    for i in range(len(list_of_lists)):
        if len(list_of_lists[i]) != len(list_of_lists):
            return None
    if len(list_of_lists[0]) == 1:
        return list_of_lists[0][0]
    elif len(list_of_lists[0]) == 2 and len(list_of_lists[1]) == 2 and len(list_of_lists) == 2:
        return list_of_lists[0][0]*list_of_lists[1][1]-list_of_lists[1][0]*list_of_lists[0][1]

    for i in range(len(list_of_lists[0])):
        newlist = list_of_lists[1:]
        for j in range(len(newlist)):
            newlist[j] = newlist[j][:i] + newlist[j][i+1:]
        det = det + ((-1)**i)*list_of_lists[0][i]*calculate_determinant(newlist)
    return det
    raise NotImplementedError
