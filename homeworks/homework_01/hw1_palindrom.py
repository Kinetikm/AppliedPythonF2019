#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    if (input_string == ''.join(reversed(input_string))):
        return True
    else:
        return False
