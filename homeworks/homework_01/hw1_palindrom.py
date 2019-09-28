#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    l = len(input_string)
    for i in range(l // 2):
        if input_string[i] != input_string[-1 - i]:
            return False
    return True
