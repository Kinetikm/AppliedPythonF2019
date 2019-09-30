#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    for i in range(len(input_lst)):
        summ = 0
        for k in range(len(input_lst) - i):
            summ += input_lst[i + k]
            if summ == num:
                return (i, i + k)
    return ()
