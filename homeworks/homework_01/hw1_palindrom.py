#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    revers_string = input_string[::-1]
    flag = input_string == revers_string
    return flag
