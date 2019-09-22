#!/usr/bin/env python
# coding: utf-8

def inver_part(input_lst, start, end):
    s = start
    e = end
    while e > s:
        k = input_lst[e]
        input_lst[e] = input_lst[s]
        input_lst[s] = k
        e -= 1
        s += 1

def word_inversion(input_lst):
    pointer = 0
    l = len(input_lst)
    for i in range(l):
        if input_lst[i] == ' ':
            inver_part(input_lst, pointer, i - 1)
            pointer = i + 1
    inver_part(input_lst, pointer, l - 1)
    return input_lst[::-1]
