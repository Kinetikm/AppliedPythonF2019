#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    s = input_lst
    s = s[::-1]
    n = len(input_lst)
    begin = 0
    end = len(s) - 1
    for i in range(n):
        if i == n - 1:
            end = i
            while begin < end:
                s[begin], s[end] = s[end], s[begin]
                begin += 1
                end -= 1
        if s[i] == ' ':
            end = i - 1
            while begin < end:
                s[begin], s[end] = s[end], s[begin]
                begin += 1
                end -= 1
            begin = i + 1
    return s
