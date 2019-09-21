#!/usr/bin/env python
# coding: utf-8


def calculate(matrix):
    det = 0
    if len(matrix) == 2:
        det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        mat = matrix[1:]
        for num, i in enumerate(matrix[0]):
            matmat = [mat[x][:num] + mat[x][num+1:] for x in range(len(mat))]
            if num % 2:
                det -= i * calculate(matmat)
            else:
                det += i * calculate(matmat)
    return det


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    a = len(list_of_lists)
    if not a:
        return None
    for i in list_of_lists:
        if len(i) != a:
            return None
    if a == 1:
        return list_of_lists[0][0]
    return calculate(list_of_lists)
