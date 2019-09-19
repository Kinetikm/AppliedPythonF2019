#!/usr/bin/env python
# coding: utf-8


def is_bracket_correct(input_string):
    '''
    Метод проверяющий является ли поданная скобочная
     последовательность правильной (скобки открываются и закрываются)
     не пересекаются
    :param input_string: строка, содержащая 6 типов скобок (,),[,],{,}
    :return: True or False
    '''
    stack = []
    d = {'{': '}', '(': ')', '[': ']'}
    for c in input_string:
        if c in d:
            stack.append(c)
        else:
            if len(stack) == 0:
                return False
            elif d[stack.pop()] == c:
                continue
            else:
                return False
    return len(stack) == 0
