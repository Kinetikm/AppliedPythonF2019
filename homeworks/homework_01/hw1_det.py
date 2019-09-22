#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    res = 1
    n = len(list_of_lists)
    for i in range(n):
        if list_of_lists[i] != n:
            return None
    for i in range(n):
        j = i
        for k in range(i + 1, n):
            if abs(list_of_lists[k][i] > abs(list_of_lists[j][i])):
                j = k
        #j = max(range(i, n), key=lambda k: abs(list_of_lists[k][i]))
        if i != j:
            list_of_lists[i], list_of_lists[j] = list_of_lists[j], list_of_lists[i]
            res *= -1
        if list_of_lists[i][i] == 0:
            return 0
        res *= list_of_lists[i][i]
        for j in range(i + 1, n):
            b = list_of_lists[j][i] / list_of_lists[i][i]
            list_of_lists[j] = [list_of_lists[j][k] - b * list_of_lists[i][k] for k in range(n)]
    return res
