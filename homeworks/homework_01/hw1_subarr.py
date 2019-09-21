#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    dc = dict()
    s = 0
    for i in range(len(input_lst)):
        s += input_lst[i]
        if (s - num == 0):
            return (0, i)
        elif (s - num) in dc:
            return(dc[s - num] + 1, i)
        else:
            dc[s] = i
    return ()
