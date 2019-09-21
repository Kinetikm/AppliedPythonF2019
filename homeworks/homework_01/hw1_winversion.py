#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    for i in range(len(input_lst)//2):
        k = input_lst[i]
        input_lst[i] = input_lst[len(input_lst) - 1 - i]
        input_lst[len(input_lst) - i - 1] = k
    start = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ' or i == len(input_lst) - 1:
            if i == len(input_lst) - 1:
                i += 1
            size_word = i - start
            for j in range(size_word // 2):
                k = input_lst[j + start]
                input_lst[j + start] = input_lst[i - 1 - j]
                input_lst[i - j - 1] = k
            start = i + 1
    print(input_lst)

str = input()
input_lst = list(str)
word_inversion(input_lst)

