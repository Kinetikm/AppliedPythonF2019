#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    s = input_string
    a = 1
    l = len(s)
    for i in range(l//2):
        if s[i] != s[l-1-i]:
            a = -1
    if a == 1:
        return True
    else:
        return False
