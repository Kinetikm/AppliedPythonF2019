#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.reverse()
    N = len(input_lst)
    begin = 0
    for i in range(0, N):
        if i == N - 1:
            end = i
            while begin < end:
                temp = input_lst[begin]
                input_lst[begin] = input_lst[end]
                input_lst[end] = temp
                end -= 1
                begin += 1

        if input_lst[i] == ' ':
            end = i - 1
            while begin < end:
                temp = input_lst[begin]
                input_lst[begin] = input_lst[end]
                input_lst[end] = temp
                end -= 1
                begin += 1
            begin = i + 1

    return input_lst
