#!/usr/bin/env python
# coding: utf-8


def is_bracket_correct(input_string):
    parentheses = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for i in input_string:
        if i in parentheses:
            stack.append(i)
        else:
            if len(stack) == 0:
                return False
            el = stack.pop()
            if parentheses[el] != i:
                return False
    return len(stack) == 0
