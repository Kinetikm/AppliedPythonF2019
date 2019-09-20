#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    k = 0
    lst = [0 for i in range(len(input_lst))]
    for k in range(len(input_lst)):
        for i in range(len(input_lst) - k):
            lst[i] += input_lst[i+k]
            if lst[i] == num:
                return i, i + k
    return ()


