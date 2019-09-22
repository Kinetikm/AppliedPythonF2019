#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    word = ''
    for i in range(len(input_lst)):
        symbol = input_lst.pop(0)
        if symbol == ' ':
            input_lst.append(word)
            word = ''
            continue
        word += symbol
    input_lst.append(word)
    input_lst.reverse()
    for i in range(len(input_lst)):
        word = input_lst.pop(0)
        for symbol in word:
            input_lst.append(symbol)
        input_lst.append(' ')
    input_lst.pop()
    return input_lst
