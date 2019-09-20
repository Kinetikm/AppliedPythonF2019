#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    for i in range(len(input_string)//2):
        if input_string[i] != input_string[-i - 1]:
            return False
    return True

