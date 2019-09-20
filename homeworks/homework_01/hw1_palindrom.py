#!/usr/bin/env python
# coding: utf-8


def check_palindrom (input_string):
    input_string = input_string.lower()
    not_l = set()
    for l in s:
        if ord("a") <= ord(l) <= ord("z"):
            continue
        else:
            input_string = input_string.replace(l, "")
    if input_string == input_string[::-1]:
        return True
    else:
        return False
