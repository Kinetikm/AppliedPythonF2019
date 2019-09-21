#!/usr/bin/env python
# coding: utf-8


def calculate_minor(num, a):
    m = []
    for i in range(1, len(a)):
        row = []
        if num == 0:
            row = a[i][1:]
        elif num == len(a) - 1:
            row = a[i][:(len(a) - 1)]
        else:
            row = a[i][:num] + a[i][num + 1:]
        m.append(row)
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    minor = 0
    for i in range(0, len(m)):
        minor += (-1) ** i * m[0][i] * calculate_minor(i, m)
    return minor


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    n = len(list_of_lists[0])
    m = len(list_of_lists)
    for i in range(0, len(list_of_lists)):
        if m != len(list_of_lists[i]):
            return None
    if n == 1:
        return list_of_lists[0][0]
    determinant = 0
    k = 1
    for i in range(n):
        determinant += list_of_lists[0][i] * \
                       calculate_minor(i, list_of_lists) * k
        k *= -1
    return determinant
