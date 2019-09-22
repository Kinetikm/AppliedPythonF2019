#!/usr/bin/env python
# coding: utf-8


def word_inversion(string):
    string.reverse()
    begin = 0
    for i in range(len(string)):
        if string[i] == " ":
            k = i - 1
            for j in range(begin, (i + begin)//2):
                string[j], string[k] = string[k], string[j]
                k = k - 1
            begin = i + 1
        if i == (len(string) - 1):
            k = i
            for j in range(begin, (i + begin) // 2):
                string[j], string[k] = string[k], string[j]
                k = k - 1
    return string
