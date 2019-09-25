#!/usr/bin/env python
# coding: utf-8


def swap(i, j, lst):
    for k in range(len(lst[i + 1:j])//2):
        lst[i + 1 + k], lst[j - 1 - k] = lst[j - 1 - k], lst[i + 1 + k]


def word_inversion(input_lst):
    input_lst.reverse()
    prm1 = -1
    prm2 = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            prm2 = i
            swap(prm1, prm2, input_lst)
            prm1 = prm2
    swap(prm1, len(input_lst), input_lst)
    return input_lst
