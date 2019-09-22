#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    dim = len(list_of_lists[0][:])
    if dim == len(list_of_lists):
        for p in range(1, len(list_of_lists)):
            if len(list_of_lists[p][:]) != dim:
                return None
    else:
        return None
    for p in range(1, dim):
        for k in range(p, dim):
            x = -list_of_lists[k][p-1]/list_of_lists[p-1][p-1]
            line = [x * el for el in list_of_lists[p-1]]
            for j in range(dim):
                list_of_lists[k][j] += line[j]
    det = 1
    for d in range(dim):
        det *= list_of_lists[d][d]
    det = round(det, 2)
    return det
