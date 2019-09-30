#!/usr/bin/env python
# coding: utf-8


def swap(i, j, lst):
    for k in range(len(lst[i + 1:j])//2):
        lst[i + 1 + k], lst[j - 1 - k] = lst[j - 1 - k], lst[i + 1 + k]


def word_inversion(input_lst):
    input_lst.reverse()
    a = -1
    b = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            b = i
            swap(a, b, input_lst)
            a = b
    swap(a, len(input_lst), input_lst)
    return input_lst
