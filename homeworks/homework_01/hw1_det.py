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
    c = 1
    d = 1
    n = len(list_of_lists)
    copy_matrix = list()
    for i in range(n):
        if len(list_of_lists[i]) != n:
            return None
    for k in range(n - 1):
        if list_of_lists[k][k] == 0:
            for q in range(k + 1, n - k):
                if list_of_lists[q][k] != 0:
                    list_of_lists[k], list_of_lists[q] = list_of_lists[q], list_of_lists[k]
                    c *= -1
                    break
        if list_of_lists[k][k] == 0:
            continue
        if k == 0:
            for p in range(k, n):
                copy_matrix.append(list_of_lists[p][k])
        else:
            for p in range(k, n):
                copy_matrix[p] = list_of_lists[p][k]
        c *= list_of_lists[k][k]
        for i in range(k, n):
            list_of_lists[k][i] /= copy_matrix[k]
            for j in range(k + 1, n):
                list_of_lists[j][i] -= list_of_lists[k][i] * copy_matrix[j]
    for i in range(n):
        d *= list_of_lists[i][i]
    return d * c
