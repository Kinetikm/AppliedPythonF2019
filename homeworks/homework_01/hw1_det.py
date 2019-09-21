#!/usr/bin/env python
# coding: utf-8


def LUP_decompose(matrix):
    CR_len = len(matrix)
    P_vec = list(range(CR_len + 1))

    for i in range(CR_len):
        max_abs = 0.0
        max_i = i

        for k in range(i, CR_len):
            cur_abs = abs(matrix[k][i])
            if cur_abs > max_abs:
                max_abs = cur_abs
                max_i = k

        if max_i != i:
            P_vec[i], P_vec[max_i] = P_vec[max_i], P_vec[i]
            matrix[i], matrix[max_i] = matrix[max_i], matrix[i]
            P_vec[CR_len] += 1

        for j in range(i + 1, CR_len):
            matrix[j][i] /= matrix[i][i]
            for k in range(i + 1, CR_len):
                matrix[j][k] -= matrix[j][i] * matrix[i][k]
    return (-1) ** (P_vec[CR_len] - CR_len)


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''

    for i in range(len(list_of_lists) - 1):
        if len(list_of_lists[i]) != len(list_of_lists[i + 1]):
            return None
    if len(list_of_lists) != len(list_of_lists[0]):
        return None

    det = 1
    sign = LUP_decompose(list_of_lists)
    for i in range(len(list_of_lists)):
        det *= list_of_lists[i][i]
    return det * sign
