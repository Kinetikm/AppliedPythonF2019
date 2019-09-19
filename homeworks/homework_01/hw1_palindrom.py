#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    help_string = list(input_string)
    help_string.reverse()
    if list(input_string) == help_string:
        return True
    return False
