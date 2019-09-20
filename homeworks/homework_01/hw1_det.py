#!/usr/bin/env python
# coding: utf-8


def kill_line(matrix, num):
    det = matrix[num][num]
    for i in range(len(matrix)):
            matrix[num][i] /= det
    for i in range(len(matrix)-num-1):
        mul = matrix[len(matrix)-i-1][num]
        for j in range(len(matrix[0])):
            matrix[len(matrix)-i-1][j] -= matrix[num][j]*mul
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
    '''Определитель находим путем приведения матрицы к диагональному виду'''
    det = 1
    if len(list_of_lists) != len(list_of_lists[0]):
            return None
    for i in range(len(list_of_lists)):
            det *= kill_line(list_of_lists, i)
    return det
