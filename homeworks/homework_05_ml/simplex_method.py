#!#!/usr/bin/env python
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
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    n, m = a.shape
    #  Создадим симплекс-таблицу
    #  где кол-во строк это кол-во неравенств n + строка c взятая с противоположным знаком,
    #  а кол-во столбцов это кол-во переменных m + кол-во строк n + 2 столбца
    sim_tab = np.zeros((n+1, m+n+2))
    result = [0 for i in range(m)]
    sim_tab[:-1, :m] = a
    sim_tab[:, m+1:] = np.eye(n+1)
    sim_tab[:-1, -1] = b
    sim_tab[-1, : m] = c[:]*(-1)
    dct = {}
    while is_negative(sim_tab, m):
        #  Найдем индекс столбца, в последней строке которого хранится
        #  наибольший отрицательный элемент
        piv_col = most_negative(sim_tab, m)
        #  Найдем индекс строки, где результат деления последнего столбца на
        #  элемент с индексом piv_col минимален
        piv_row = smallest_quotient(sim_tab, piv_col)
        dct[piv_row] = piv_col
        sim_tab[piv_row][:] = sim_tab[piv_row] / sim_tab[piv_row][piv_col]
        for i in range(n+1):
            if i != piv_row:
                sim_tab[i][:] = sim_tab[i][:] - sim_tab[piv_row][:]*sim_tab[i][piv_col]
    for key, value in dct.items():
        result[value] = sim_tab[key][-1]
    return np.array(result)


def is_negative(sim_tab, m):
    for i in range(m):
        if sim_tab[-1][i] < 0:
            return True
    else:
        return False


def most_negative(sim_tab, m):
    p = 1
    ind = -1
    for i in range(m):
        if sim_tab[-1][i] < p:
            ind = i
            p = sim_tab[-1][i]
    return ind


def smallest_quotient(sim_tab, piv_col):
    p = np.sum(sim_tab[:-1][-1])*100
    ind = -1
    for i in range(sim_tab.shape[0]-1):
        k = sim_tab[i][sim_tab.shape[1]-1]/sim_tab[i][piv_col]
        if k < p:
            ind = i
            p = k
    return ind
