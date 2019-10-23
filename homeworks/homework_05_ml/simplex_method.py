#!/usr/bin/env python
# coding: utf-8

import numpy as np


def prepare_matrix_to_simplex_method(coef_matrix, free_memb, max_eq):
    """
    :param max_eq:np.array, shape=(1, n) Максимизируемая функция. Размерность: 1 x m
    :param coef_matrix:np.array, shape=(n, m) Матрица коэффициентов системы неравенств. Размерность: n x m
    :param free_memb:np.array, shape=(n, 1) Свободные члены системы неравенств. Размерность: n x 1
    :return prep_matrix:np.array, shape=(n+1, m+n+1)
    """
    prep_matrix = np.vstack((coef_matrix, (-1) * max_eq))
    prep_matrix = np.hstack((prep_matrix, np.eye(prep_matrix.shape[0])))
    prep_matrix = np.hstack((prep_matrix, np.append(free_memb, 0).reshape(prep_matrix.shape[0], 1)))
    return prep_matrix


def simplex_method(a, b, c):
    """
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """
    simp_matr = prepare_matrix_to_simplex_method(a, b, c)
    swap_save = np.full(a.shape[0], -1)

    while not all(simp_matr[-1] >= 0):
        pivot_col = simp_matr[-1].argmin()
        repl_item_row = (simp_matr[: len(simp_matr) - 1, -1] / simp_matr[: len(simp_matr) - 1, pivot_col]).argmin()
        simp_matr[repl_item_row, :] = simp_matr[repl_item_row, :] / simp_matr[repl_item_row, pivot_col]
        for row in range(len(simp_matr)):
            if row == repl_item_row:
                continue
            koef = simp_matr[row, pivot_col] / simp_matr[repl_item_row, pivot_col]
            simp_matr[row, :] = simp_matr[row, :] - (simp_matr[repl_item_row, :] * koef)
            swap_save[repl_item_row] = pivot_col

    target_function = np.zeros(a.shape[1])

    for i, index_el in enumerate(swap_save):
        if index_el != -1:
            target_function[index_el] = simp_matr[i, -1]

    return target_function
