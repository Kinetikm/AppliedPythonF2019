#!/usr/bin/env python
# coding: utf-8


def calculate_determinant(list_of_lists):
    def new_matrix(line, column, lst):
        temp = []
        add = 0
        for k in range(len(lst)):
            if k == line:
                add = 1
                continue
            temp += [[]]
            for j in range(len(lst)):
                if j == column:
                    continue
                temp[k - add] += [lst[k][j]]
        return temp

    if len(list_of_lists) != len(list_of_lists[0]):
        return None

    if len(list_of_lists) == 1:
        return list_of_lists[0][0]

    res = 0
    for i in range(len(list_of_lists)):
        res += (-1)**(i % 2) * list_of_lists[0][i] * calculate_determinant(new_matrix(0, i, list_of_lists))
    return res
