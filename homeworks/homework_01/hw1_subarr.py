#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    d = {}
    s = 0
    for i, val in enumerate(input_lst):
        s += val
        if s - num in d:
            return (d[s - num], i)
        elif val == num:
            return (i,i)
        else:
            d[s - val] = i
    return ()

a = [9, 2, 3, 4, 5, -2, 8]
print(find_subarr(a, 6))
