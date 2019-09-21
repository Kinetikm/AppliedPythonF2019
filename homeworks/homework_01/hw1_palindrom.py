#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    size = len(input_string)
    for i in range(size // 2):
        if input_string[i] != input_string[size - 1 - i]:
            return False
    return True
