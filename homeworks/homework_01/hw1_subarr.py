#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    if len(input_lst) != 0:
        if input_lst[0] == num:
            return tuple((0, 0))
        p = [0] * len(input_lst)
        d = {}
        p[0] = input_lst[0]
        for i in range(1, len(input_lst)):
            if input_lst[i] == num:
                return tuple((i, i))
            p[i] += p[i - 1] + input_lst[i]
            if p[i] == num:
                return tuple((0, i))
        for i in range(len(input_lst)):
            d[num - p[i]] = i
        for i in range(len(input_lst)):
            if ((-1 * p[i]) in d) and i + 1 < d[-1 * p[i]]:
                return tuple((i + 1, d[-1 * p[i]]))
        return tuple()
    else:
        return tuple()
