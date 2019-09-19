#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    if len(input_lst) > 0:
        input_lst[0] = "".join(input_lst).split()
        input_lst[0].reverse()
        input_lst[0] = list(" ".join(input_lst[0]))
        for i in range(len(input_lst) - 1, -1, -1):
            input_lst[i] = input_lst[0][i]
    return input_lst
    # можно возвращать None, все равно будет работать
