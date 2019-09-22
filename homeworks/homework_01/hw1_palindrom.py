#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    q = input_string[::-1]
    return input_string == q
