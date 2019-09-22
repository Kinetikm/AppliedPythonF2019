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
    def new_minor(list_of_lists, i, j):
        min = []
        for n_1, row in enumerate(list_of_lists):
            if n_1 != i:
                min.append([col for n_2, col in enumerate(row) if n_2 != j])
        return min

    n = len(list_of_lists)
    
    if n < 1:
        return None
    if n == 1:
        return list_of_lists[0][0]
    for row in range(n):
        if len(list_of_lists[row]) != n:
            return None
    
    det = 0
    for i in range(n):
        minor = new_minor(list_of_lists, 0, i)
        det += ((-1) ** (1+i+1)) * list_of_lists[0][i] * calculate_determinant(minor)
        
    return det
