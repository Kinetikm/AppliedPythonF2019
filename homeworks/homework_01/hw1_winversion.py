#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    l = input_lst
    i = 0
    k = 0
    while i < len(l):
        j = i
        if l[j] == ' ':
            while j > 0:
                l[j], l[j - 1] = l[j - 1], l[j]
                j -= 1
            i += 1
            k = 0
        else:
            while j > k:
                l[j], l[j - 1] = l[j - 1], l[j]
                j -= 1
            i += 1
            k += 1
    return l
