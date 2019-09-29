#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    k = 0
    revers_from_to(input_lst, 0, len(input_lst) - 1)
    for i in range(len(input_lst)):
        if input_lst[i] == " ":
            revers_from_to(input_lst, k, i - 1)
            k = i + 1
    revers_from_to(input_lst, k, len(input_lst) - 1)
    return input_lst


def revers_from_to(input_lst, first, second):
    for i in range(0, (second - first + 1) // 2):
        k = input_lst[first + i]
        input_lst[first + i] = input_lst[second - i]
        input_lst[second - i] = k
