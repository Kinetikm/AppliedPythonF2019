#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    match = 0
    l = len(input_string)
    for i in range(l // 2):
        if input_string[i] == input_string[l - 1 - i]:
            match += 1
    if match == l // 2:
        return True
    else:
        return False
