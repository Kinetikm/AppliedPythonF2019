#!/usr/bin/env python
# coding: utf-8


def word_inversion(inputl):
    leng = len(inputl)
    for i in range(leng // 2):
        inputl[i], inputl[leng-1-i] = inputl[leng-1-i], inputl[i]
    begin = 0
    end = 0
    i = 1
    while i < leng:
        while (inputl[i] != ' '):
            end += 1
            i += 1
            if i >= leng:
                break
        word = end - begin + 1
        for p in range(word // 2):
            inputl[p+begin], inputl[end-p] = inputl[end-p], inputl[p+begin]
        end += 2
        begin = end
        i += 2
    return inputl
