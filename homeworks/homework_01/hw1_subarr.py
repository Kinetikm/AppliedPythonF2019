#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    if len(input_lst) == 0:
        return ()
    t = input_lst[0]
    for i in range(1, len(input_lst)):
        if (num == input_lst[i]):
            return (i, i)
        elif (num == t + input_lst[i]):
            return (i-1, i)
        t = input_lst[i]
    return ()