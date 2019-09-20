#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst.append(' ')
    word = ''
    for i in range(len(input_lst)):
        ch = input_lst.pop(0)
        word += ch
        if ch == ' ':
            input_lst.append(word[:-1])
            word = ''
    input_lst.reverse()
    for i in range(len(input_lst)):
        word = input_lst.pop(0)
        for ch in word:
            input_lst.append(ch)
        input_lst.append(' ')
    input_lst.pop()
    return input_lst
