#!/usr/bin/env python
# coding: utf-8

import numpy as np


def min_search(row):
    min = row[0]
    min_pos = 0
    for i in range(len(row)):
        if row[i] < min:
            min = row[i]
            min_pos = i
    return min, min_pos


def smplx_iteration(matrix, pivot_col, var_list):
    #  find row
    min_div = matrix[0, matrix.shape[1] - 1] / matrix[0, pivot_col]
    pivot_row = 0
    for i in range(matrix.shape[0] - 1):
        dr = matrix[i, matrix.shape[1] - 1] / matrix[i, pivot_col]
        if (dr > 0) and (dr < min_div):
            min_div = dr
            pivot_row = i
    var_list[pivot_row] = pivot_col
    matrix[pivot_row, ] = matrix[pivot_row, ] / matrix[pivot_row, pivot_col]
    for i in range(matrix.shape[0]):
        if i != pivot_row:
            matrix[i, ] = matrix[i, ] - matrix[pivot_row, ] * matrix[i, pivot_col]
    return matrix, var_list


def simplex_method(a, b, c):
    nb = np.zeros((len(b), 1))
    for i in range(len(b)):
        nb[i, 0] = b[i]
#  create simplex matrix
    smplx_matr = np.array(a)
    smplx_matr = np.concatenate((smplx_matr, np.eye(a.shape[0])), axis=1)
    p = np.zeros((a.shape[0], 1))
    smplx_matr = np.concatenate((smplx_matr, p), axis=1)
    smplx_matr = np.concatenate((smplx_matr, nb), axis=1)
    tail_row = np.zeros((1, a.shape[0] + a.shape[1] + 2))
    tail_row[0, :a.shape[1]] = -c[::]
    tail_row[0, a.shape[0] + a.shape[1]] = 1
    smplx_matr = np.concatenate((smplx_matr, tail_row), axis=0)
    var_list = [i for i in range(a.shape[1], a.shape[1] + a.shape[0])]


#  start
    minimum = min_search(smplx_matr[smplx_matr.shape[0] - 1])
    while minimum[0] < 0:
        cur_res = smplx_iteration(smplx_matr, minimum[1], var_list)
        smplx_matr = cur_res[0]
        var_list = cur_res[1]
        minimum = min_search(smplx_matr[smplx_matr.shape[0] - 1])
    res = [0] * a.shape[1]
    for i in range(len(var_list)):
        if var_list[i] < a.shape[1]:
            res[var_list[i]] = smplx_matr[i, smplx_matr.shape[1] - 1]
    return res
