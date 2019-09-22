#!/usr/bin/env python
# coding: utf-8


def substract(x, y, k):
    for i in range(len(x)):
        x[i] -= y[i]*k


def is_zero(matr, d):
    m, n = -1, -1
    if matr[d][d] != 0:
        return 1
    else:
        for i in range(d, len(matr)):
            for j in range(d, len(matr)):
                if matr[i][j] != 0:
                    m, n = i, j
        if m == -1 and n == -1:
            return 0
        for i in range(len(matr)):
            matr[d][i], matr[m][i] = matr[m][i], matr[d][i]
        matr[d][d], matr[d][n] = matr[d][n], matr[d][d]
        if d == m and d == n:
            return 1
        else:
            return -1


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    n = len(list_of_lists)
    flag = True
    i, j, k = 0, 0, 1
    for i in range(n):
        if len(list_of_lists[i]) != n:
            flag = False
    if not flag:
        return None
    else:
        for i in range(n-1):
            k *= is_zero(list_of_lists, i)
            if k == 0:
                return 0
            for j in range(i+1, n):
                c = list_of_lists[j][i] / list_of_lists[i][i]
                substract(list_of_lists[j], list_of_lists[i], c)
        det = 1
        for i in range(n):
            det *= list_of_lists[i][i]
        return det * k
