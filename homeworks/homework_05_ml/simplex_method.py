#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://  https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(m, n)
    :param b: np.array, shape=(m, 1)
    :param c: np.array, shape=(1, n)
    :return x: np.array, shape=(1, n)
    """
    m, n = a.shape
    #  Создадим симплекс-таблицу,
    #  где кол-во строк это кол-во неравенств m + строка c взятая с противоположным знаком,
    #  а кол-во столбцов это кол-во переменных n + кол-во строк m + 2 столбца
    sim_tab = np.zeros((m+1, m+n+2))
    result = np.zeros((1, n))
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            sim_tab[i][j] = a[i][j]
    for i in range(m+1):
        for j in range(n, n+m+1):
            sim_tab[i][n+j] = 1
    for i in range(m+1):
        a[i][n+m+1] = b[i][0]
    for j in range(n):
        a[m][j] = (-1)*c[0][j]
    lst = ['0' for i in range(m)]
    while is_negative(sim_tab, n):
        #  Найдем индекс столбца, в последней строке которого хранится
        #  наибольший отрицательный элемент
        piv_col = most_negative(sim_tab, n)
        #  Найдем индекс строки, где результат деления последнего столбца на
        #  элемент с индексом piv_col минимален
        piv_row = smallest_quotient(sim_tab, piv_col)
        row = [sim_tab[i][:] for i in range(m+1)]
        row[piv_row] = row / row[piv_row][piv_col]
        lst[piv_row] = pivet_col
        for i in range(m+1):
            if i != piv_row:
                row[i] -= row[piv_row]*row[i][piv_col]
        for i in range(m+1):
            sim_tab[i][:] = row[i]
    for i in lst:
        if lst[i] != '0':
            result[element] = sim_tab[i][-1]
    return result


def is_negative(sim_tab, n):
    for i in range(n):
        if sim_tab.shape[0][i] < 0:
            return True
    else:
        return False


def most_negative(sim_tab, n):
    p = 1
    ind = -1
    for i in range(n):
        if sim_tab[n][i] < p:
            ind = i
            p = sim_tab[n][i]
    return ind


def smallest_quotient(sim_tab, piv_col):
    p = np.sum(sim_tab[:-1][-1])*100
    ind = -1
    for i in range(sim_tab.shape[0]-1):
        k = sim_tab[i][sim_tab.shape[1]]/sim_tab[i][piv_col]
        if k < p:
            ind = i
            p = k
    return ind
