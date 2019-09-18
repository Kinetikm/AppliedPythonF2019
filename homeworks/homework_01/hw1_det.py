#!/usr/bin/env python
# coding: utf-8
import math


def calculate_determinant(list_of_lists):
    """
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    """
    n = len(list_of_lists)
    m = len(list_of_lists[0])
    if n != m:
        return None  # матрица не квадаратная

    # сводим матрицу к диагональному виду (метод Гауса)
    det = 1
    for i in range(n):
        #  Ищем pivot элемент в столбце i строках j > i
        pivot = i
        for j in range(i + 1, n):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[pivot][i]):
                pivot = j
        if math.isclose(list_of_lists[pivot][i], 0):
            return 0
        #  переставляем pivot в i-ую строку
        list_of_lists[i], list_of_lists[pivot] = list_of_lists[pivot], list_of_lists[i]
        if i != pivot:
            det *= -1  # определитель меняет знак если переставляем местами строки
        det *= list_of_lists[i][i]
        pivot_element = list_of_lists[i][i]
        for j in range(i, n):
            list_of_lists[i][j] /= pivot_element
        for j in range(i+1, n):
            if not math.isclose(list_of_lists[j][i], 0):
                diag_element = list_of_lists[j][i]
                for k in range(i, n):
                    list_of_lists[j][k] -= list_of_lists[i][k] * diag_element
    return det
