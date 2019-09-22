#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    n = len(list_of_lists)
    for _, lst in enumerate(list_of_lists):
        if len(lst) != n:
            return None
    if len(list_of_lists) == 1:
        return list_of_lists[0][0]
    return det(list_of_lists)


def det_low(mat, num):
    res = list()
    for i in range(1, len(mat)):
        cur_str = mat[i][:num]
        cur_str.extend(mat[i][num+1:])
        res.append(cur_str)
    return res


def det(mat):
    if len(mat) == 2:
        return mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1]
    sum = 0
    sign = 1
    for i in range(len(mat)):
        sum += sign * mat[0][i] * det(det_low(mat, i))
        sign = -sign
    return sum
