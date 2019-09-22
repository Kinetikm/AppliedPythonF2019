#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    d = dict()
    s = 0
    for i, v in enumerate(input_lst):
        s = s + v
        if s == num:
            return 0, i
        if s - num in d:
            return d[s-num]+1, i
        d[s] = i
