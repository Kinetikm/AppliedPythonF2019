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
    if not is_square_matrix_check(list_of_lists):
        return None
    elif len(list_of_lists) == 1:
        return list_of_lists[0][0]
    elif len(list_of_lists) == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[1][0] * list_of_lists[0][1]
    else:
        determinant = 0
        for i in range(len(list_of_lists)):
            sub_matrix = []
            for j in range(len(list_of_lists)):
                if i != j:
                    sub_matrix.append(list_of_lists[j][1:])
            minor = calculate_determinant(sub_matrix)
            determinant += list_of_lists[i][0] * ((-1) ** (0 + i)) * minor
        return determinant

def is_square_matrix_check(matrix):
    for i, val in enumerate(matrix):
        if len(matrix) != len(matrix[i]):
            return False
    return True
