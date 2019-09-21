#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    size = len(input_lst)
    for i in range(size // 2):
        input_lst[i], input_lst[size - 1 - i] = input_lst[size - 1 - i], input_lst[i]
    print(input_lst)
    a = 0
    for i in range(size):
        if input_lst[i] == ' ' or i == size - 1:
            if i == size - 1:
                i += 1
            size_1 = i - a
            for j in range(size_1 // 2):
                input_lst[j + a], input_lst[i - 1 - j] = input_lst[i - 1 - j], input_lst[j + a]
            a = i + 1
            print(a)
        print(input_lst)
    return input_lst
