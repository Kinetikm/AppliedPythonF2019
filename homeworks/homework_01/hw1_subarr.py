#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):
    for i in range(len(input_lst)):
        for j in range(i, len(input_lst)):
            if (sum(input_lst[i:j + 1]) == num):
                return (i, j)
    return ()
