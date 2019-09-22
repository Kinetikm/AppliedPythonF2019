#!/usr/bin/env python
# coding: utf-8


def action(a, b, k):
    for i in range(len(a)):
        a[i] -= b[i]*k


def check_zero(a, d):
    m, n = -1, -1
    if a[d][d] != 0:
        return 1
    else:
        for i in range(d, len(a)):
            for j in range(d, len(a)):
                if a[i][j] != 0:
                    m, n = i, j
        if m == -1 and n == -1:
            return 0
        for i in range(len(a)):
            a[d][i], a[m][i] = a[m][i], a[d][i]
        a[d][d], a[d][n] = a[d][n], a[d][d]
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
    a = list_of_lists
    n = len(a)
    flag = True
    i, j, k = 0, 0, 1
    for i in range(n):
        if len(a[i]) != n:
            flag = False
    if not flag:
        return None
    else:
        for i in range(n-1):
            k *= check_zero(a, i)
            if k == 0:
                return 0
            for j in range(i+1, n):
                c = a[j][i] / a[i][i]
                action(a[j], a[i], c)
        det = 1
        for i in range(n):
            det *= a[i][i]
        return det * k
