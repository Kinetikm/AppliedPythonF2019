#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    input_string = "ertre"
    string = input_string[::-1]
    if string == input_string:
        print("True")
    else:
        print("False")
    raise NotImplementedError
