#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    for j in range(len(input_lst) - 1):
        if input_lst[j] == num:
            return j, j
        if (input_lst[j] + input_lst[j + 1]) == num:
            returnj, j + 1
    return()
