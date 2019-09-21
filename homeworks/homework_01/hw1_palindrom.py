#!/usr/bin/env python
# coding: utf-8


def check_palindrom (input_string):
    a = input_string == input_string[::-1]
    return a
