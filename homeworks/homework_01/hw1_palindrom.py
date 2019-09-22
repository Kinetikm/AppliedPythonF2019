#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    a = input_string[::-1]
    if input_string == a:
        return True
    else:
        return False
