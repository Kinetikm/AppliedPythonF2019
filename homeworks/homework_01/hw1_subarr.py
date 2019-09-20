#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    d = {}
    s = 0
    for i in range(len(input_lst)):
        s += input_lst[i]
        if s == num:
            return (0, i)
        try:
            j = d[s - num]
        except KeyError:
            pass
        else:
            return (j + 1, i)
        d[s] = i
    return ()
