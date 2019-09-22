#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    str_tmp = input_string[::-1]
    if input_string == str_tmp:
        return True
    else:
        return False
