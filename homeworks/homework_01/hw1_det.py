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
    def minor(list_of_lists , i , j):
        min = []
        for ln1,row in enumerate(list_of_lists):
            if ln1 != i:
                min.append([col for ln2 , col in enumerate(row) if ln2 != j])
        return min

    det = 0
    ln = len(list_of_lists)
    if ln== 1:
        return list_of_lists[0][0]
    for row in range(ln):
        if len(list_of_lists[row]) != ln:
            return None
    for i in range(ln):
        min = minor(list_of_lists,0,i)
        det = det + (((-1) ** (2+i)) * calculate_determinant(min) * list_of_lists[0][i] )
    return det
    raise NotImplementedError
