#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    dc = dict()
    for i in range(len(input_lst)):
        k = sum(input_lst[:i + 1])
        if (k - num == 0):
            return (0, i)
        elif (k - num) in dc:
            return(dc[k - num] + 1, i)
        else:
            dc[k] = i
    return ()
