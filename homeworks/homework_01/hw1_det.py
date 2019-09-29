#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    res = 1
    eps = 1e-15
    n = len(list_of_lists)
    for i in range(n):
        if len(list_of_lists[i]) != n:
            return None
    for i in range(n):
        m = i
        for j in range(i + 1, n):
            if abs(list_of_lists[j][i]) > abs(list_of_lists[m][i]):
                m = j
        if abs(list_of_lists[m][i]) < eps:
            return 0
        list_of_lists[i], list_of_lists[m] = list_of_lists[m], list_of_lists[i]
        if i != m:
            res *= -1
        res *= list_of_lists[i][i]
        for j in range(i + 1, n):
            list_of_lists[i][j] /= list_of_lists[i][i]
        for j in range(n):
            if j != i and abs(list_of_lists[j][i]) > eps:
                for k in range(i + 1, n):
                    list_of_lists[j][k] -= list_of_lists[i][k] * list_of_lists[j][i]
    return res