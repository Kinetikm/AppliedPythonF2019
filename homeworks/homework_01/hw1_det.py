#!/usr/bin/env python
# coding: utf-8
import copy


def minor(a, i, j):
    m = copy.deepcopy(a)
    for k in range(len(a)):
        del m[k][j]
    del m[i]
    return m
# метод по созданию минора матрицы по данным строке и столбцу
# копирует матрицу, и в ней удаляет строку и столбец


def calculate_determinant(a):
    m = len(a)
    n = len(a[0])
    if m != n:
        return None
    elif n == 1:
        return a[0][0]
    sign = 1
    # при вычислении алгебраических дополнений знак в зависимости
    # от четности строки и столбца изменяется
    det = 0
    for i in range(n):
        det += a[0][i] * sign * calculate_determinant(minor(a, 0, i))
        sign *= -1
    return det
# метод нахождения определителя матрицы методом разложения по строке
