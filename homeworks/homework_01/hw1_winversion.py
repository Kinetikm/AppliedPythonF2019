#!/usr/bin/env python
# coding: utf-8


def word_inversion(x):
    if len(x) < 2:
        return None
    mark = 0
    for elem, i in zip(x, range(len(x))):
        if elem == ' ':
            x[mark: i] = x[mark:i][::-1]
            mark = i + 1
    x[mark: len(x)] = x[mark: len(x)][::-1]
    return x[::-1]
