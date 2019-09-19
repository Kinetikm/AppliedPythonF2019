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

    def create_minor(list_of_lists, i, j):
        minor = []
        for m, row in enumerate(list_of_lists):
            if m == i:
                continue
            minor.append([e for n, e in enumerate(row) if n != j])
        return minor

    m = len(list_of_lists)
    for row in list_of_lists:
        if len(row) != m:
            return None
    if m == 1:
        return list_of_lists[0][0]
    i = 0
    s = 0
    for j, a in enumerate(list_of_lists[i]):
        minor = create_minor(list_of_lists, i, j)
        s += a * ((-1) ** (i + j)) * calculate_determinant(minor)
    return s
