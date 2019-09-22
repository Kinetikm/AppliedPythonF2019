#!/usr/bin/env python
# coding: utf-8


def winversion(input_lst, a, b):
    while b - a > 0:
        t = input_lst[a]
        input_lst[a] = input_lst[b]
        input_lst[b] = t
        a += 1
        b -= 1


def word_inversion(input_lst):
    a = 0
    i = 0
    while i <= len(input_lst):
        if i == len(input_lst) or input_lst[i] == ' ':
            winversion(input_lst, a, i - 1)
            a = i + 1
        i += 1
    winversion(input_lst, 0, len(input_lst) - 1)
    return input_lst
