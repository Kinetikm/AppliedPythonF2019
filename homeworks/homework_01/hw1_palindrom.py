#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    length = len(input_string)
    for i in range(length//2):
        if input_string[i] != input_string[length - 1 - i]:
            return False
    return True
