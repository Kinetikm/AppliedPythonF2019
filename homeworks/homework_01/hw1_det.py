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
    # Check if matrix has appropriate dimensions
    def check_dims(m):
        if not isinstance(m, list):
            return False
        if len(list_of_lists) == 0:
            return False
        ret_val = True
        for line in m:
            if not isinstance(line, list) or len(line) != len(m):
                ret_val &= False
                break
        return ret_val

    # Exclude defined row and column from given matrix.
    # All indices start from from 0

    def exclude(matrix, i, j):
        ret_matrix = copy.deepcopy(matrix)
        ret_matrix.pop(i)
        for m, _ in enumerate(ret_matrix):
            ret_matrix[m].pop(j)
        return ret_matrix

    if not check_dims(list_of_lists):
        return None

    if len(list_of_lists) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]

    if len(list_of_lists) == 1:
        return list_of_lists[0][0]

    det = 0
    k = 1
    for n, item in enumerate(list_of_lists[0]):
        det += k * item * calculate_determinant(exclude(list_of_lists, 0, n))
        k *= -1
    return det
