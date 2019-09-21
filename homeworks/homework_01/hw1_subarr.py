#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    ind = {}
    summ = 0
    for i in range(len(input_lst)):
        summ += input_lst[i]
        ind[summ] = i
        if (summ - num) in ind:
            return (ind[summ - num] + 1, i)

        elif summ == num:
            return (0, i)
    return ()
