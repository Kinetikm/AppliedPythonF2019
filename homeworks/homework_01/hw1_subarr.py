#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    dct = {}
    s = 0
    for i in range(len(input_lst)):
        s += input_lst[i]
        if s == num:
            return (0, i)
        if (s - num) in dct:
            return (dct[s - num] + 1, i)
        dct[s] = i
    return ()
