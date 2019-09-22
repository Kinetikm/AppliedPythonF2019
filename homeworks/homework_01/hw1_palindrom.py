#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    if len(input_string) == 0:
        return False
    for i in range(len(input_string)//2):
        if input_string[i] != input_string[-1-i]:
            return False
    return True
