#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    if input_string[::] == input_string[::-1]:
        answer = True
    else:
        answer = False
    return answer
