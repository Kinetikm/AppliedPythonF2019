#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    i = 0
    while i <= len(input_lst) - 1:
        sum = 0
        j = i
        while j <= len(input_lst) - 1:
            sum += input_lst[j]
            if sum == num:
                return i, j
            j += 1
        i += 1
    return ()
