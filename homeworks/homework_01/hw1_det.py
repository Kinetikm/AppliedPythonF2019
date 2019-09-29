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
    def findTable(table, i, j):
        t1 = []
        t2 = []
        n = 0
        for k in table:
            if n != i:
                t2 = k[::]
                t2.pop(j)
                t1.append(t2[::])
            n = n + 1
        return t1
    
    def findDet(table):
        size = len(table)
        i = 0
        d = 0
        k = 1
        if size == 1:
            d = table[0][0]
            return d
        if size == 2:
            d = table[0][0] * table[1][1] - table[0][1] * table[1][0]
            return d
        while i != size:
            t = findTable(table, 0, i)
            d = d + k * table[0][i] * findDet(t)
            k = -k
            i = i + 1
        return d
    l = len(list_of_lists)
    for i in list_of_lists:
        if len(i) != l:
            return None
    d = findDet(list_of_lists)
    return d
    raise NotImplementedError
