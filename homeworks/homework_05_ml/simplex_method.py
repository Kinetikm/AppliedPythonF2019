#!/usr/bin/env python
# coding: utf-8

import numpy as np


def init_array(a, b, c):
    """ p_array =
    [[a11, .., a1m, s1(m+1), .., s1(m + n + 1), b1]
     [...                                         ]
     [an1, .., anm, sn(m+1), .., sn(m + n + 1), bn]]
     where s[:,m + 1: m + n + 1] - дополнительные базисные элементы
    """
    n, m = a.shape
    p_array = np.zeros((n + 1, m + n + 1 + 1), dtype=float)

    p_array[0:n, 0:m] = a
    p_array[n, 0:m] = -c
    p_array[0:, m:m + n + 1] = np.eye(n + 1)
    p_array[0:n, -1] = b[:]
    return p_array


def get_min_bottom_element(column):
    j_min = column.argmin()
    min_el = column[j_min]
    return j_min, min_el


def get_x(p_array, m):
    x = np.array(p_array[-1, 0:m])
    # идем вдоль последней строки иксов, если встретили не 0,
    # значит x[j] = 0, иначе - брать значения из самой последней колонки.
    for j in range(m):
        if p_array[-1, j] != 0:
            x[j] = 0
        else:
            # у нас гарантировано в колонке одна 1 и все остальные 0,
            # скалярное произведение даст нужный элемент.
            x[j] = p_array[:, -1].dot(p_array[:, j].T)
    return x


def get_pivot_ij(p_array, j_min):
    """
    :param p_array: np.array, shape=(n + 1, m + n + 1 + 1)
    :param j_min: int, index of the smallest negative element in p_array[-1]
    :return (i_pivot, j_pivot): row and column of pivot element
    """
    b = p_array[:-1, -1]
    pivot_column = p_array[:-1, j_min]
    b_div = b / pivot_column
    i_pivot = b_div.argmin()
    j_pivot = j_min

    return i_pivot, j_pivot


def array_transform(p_array, i_pivot, j_pivot):
    """
    :param p_array: np.array, shape=(n + 1, m + n + 1 + 1)
    :param (i_pivot, j_pivot): row and column of pivot element
    :return p_array
    """
    pivot = p_array[i_pivot, j_pivot]
    # делим всю опорную строку на опорный элемент
    p_array[i_pivot, :] /= pivot
    # меняем местами опорную строку и самую первую, чтобы слайсом можно было идти слайсом, исключая опорную строку.
    tmp = np.array(p_array[i_pivot, :])
    p_array[i_pivot, :] = p_array[0, :]
    p_array[0, :] = tmp

    # массив коэффициентов для соответствующей строки, домножив опорную на которые,
    # можно будет сложить с соответс. строками
    # чтобы обнулить значения в опорной колонке (шаг алгоритма)
    coeff = np.array([-p_array[1:, j_pivot]]).T
    p_array[1:, :] = coeff * p_array[0, :] + p_array[1:, :]

    return p_array


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
    np.set_printoptions(suppress=True)
    n, m = a.shape
    p_array = init_array(a, b, c)
    j_min, min_el = get_min_bottom_element(p_array[-1])

    while(min_el < 0):
        i_pivot, j_pivot = get_pivot_ij(p_array, j_min)
        p_array = array_transform(p_array, i_pivot, j_pivot)
        j_min, min_el = get_min_bottom_element(p_array[-1])

    return get_x(p_array, m)
