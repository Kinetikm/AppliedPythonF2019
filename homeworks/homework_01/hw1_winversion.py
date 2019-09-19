#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    a = ['i', 'p', ' ', 'i', ' ', 'e', 'h', 'j']
    b = a[::-1]
    arr = []
    i = 0
    l = 0
    while i <= len(b) - 1:
        k = len(a) - i
        if b[i] == ' ':
            c = a[k:len(a) - l:]
            arr.append(c)
            l == i
        i += 1
    print (c)
    raise NotImplementedError
