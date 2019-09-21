#!/usr/bin/env python
# coding: utf-8

def minor(A, i, j):
    M = copy.deepcopy(A)  # копирование!
    del M[i]
    for i in range(len(A[0]) - 1):
        del M[i][j]
    return M

def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    m = len(list_of_lists)
    n = len(list_of_lists[0])

    if m != n:
        return None
    if n == 1:
        return list_of_lists[0][0]

    signum = 1
    determinant = 0
    # разложение по первой строке
    for j in range(n):
        determinant += list_of_lists[0][j] * signum * calculate_determinant(minor(list_of_lists, 0, j))
        signum *= -1

    return determinant
    
    raise NotImplementedError
