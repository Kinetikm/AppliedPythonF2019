#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    if len(list_of_lists) != len(list_of_lists[0]):
        return None

    def minor(line, col, lst):
        temp = []
        size1 = len(lst)
        add = 0
        for k in range(size1):
            if k == line:
                add = 1
                continue
            temp += [[]]
            for j in range(size1):
                if j == col:
                    continue
                temp[k - add] += [lst[k][j]]
        return temp
    res = 0
    size = len(list_of_lists)
    if size == 1:
        return list_of_lists[0][0]
    if size == 2:
        return list_of_lists[0][0] * list_of_lists[1][1] - list_of_lists[0][1] * list_of_lists[1][0]
    for i in range(size):
        m = minor(0, i, list_of_lists)
        det = calculate_determinant(m)
        res += (-1)**i * list_of_lists[0][i] * det
    return res
