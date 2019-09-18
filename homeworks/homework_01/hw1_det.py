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
    A = list_of_lists
    n = len(A)
    m = len(A[0])
    if n!=m:
        return None
    if n == 1:
        return A[0]
    else:
        for i in range(n): #номер шага и номер вычитаемой строки
            for j in range(n-1, i, -1):  #номер строки n-1..0
                if A[i][i]!=0:
                    koeff = (A[j][i]/A[i][i])
                else:
                    koeff = 0
                for k in range(n):   #индексы в j строке
                    A[j][k] = A[j][k] - koeff * A[i][k]
        det = 1
        for i in range(n):
            det*=A[i][i]
        return det
