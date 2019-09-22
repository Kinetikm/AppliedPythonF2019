#!/usr/bin/env python
# coding: utf-8


def find_subarr(input_lst, num):

    s = 0
    for i in range(len(input_lst)):
        if input_lst[i] > num:
            s = 0
            continue
        if input_lst[i] == num:
            return (i, i)
        s = input_lst[i]
        for j in range(i + 1, len(input_lst)):
            if input_lst[j] > num:
                s = 0
                break
                if input_lst[j] == num:
                    return (j, j)
            else:
                s = s + input_lst[j]
                if s == num:
                    return (i, j)
        s = 0
    return ()