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
