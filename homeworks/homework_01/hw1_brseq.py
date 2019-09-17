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
    opened_bracket = []
    open_bracket = ['(', '[', '{']
    close_bracket = [')', ']', '}']
    for i in input_string:
        if i in open_bracket:
            opened_bracket.append(i)
        elif i in close_bracket and len(opened_bracket) == 0:
            return False
        elif i in close_bracket and opened_bracket[-1] == open_bracket[
            close_bracket.index(i)]:
            opened_bracket.pop()
        else:
            return False
    return True
    raise NotImplementedError
