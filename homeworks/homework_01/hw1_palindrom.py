#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    copy_string = list(input_string)
    copy_string.reverse()
    input_string = list(input_string)
    if input_string == copy_string:
        return True
    else:
        return False
