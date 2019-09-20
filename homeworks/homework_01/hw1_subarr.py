#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    if len(input_lst) == 1:
        if input_lst[i] == num:
            return i
        else:
            return()

    for i in range(len(input_lst) - 1):
        if input_lst[i] == num:
            return i, i
        if (input_lst[i] + input_lst[i + 1]) == num:
            return i, i + 1
    return()
