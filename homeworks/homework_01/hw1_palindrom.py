#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    '''
    Метод проверяющий строку на то, является ли
    она палиндромом.
    :param input_string: строка
    :return: True, если строка являестя палиндромом
    False иначе
    '''
    l = len(input_string)
    hl = l // 2
    for i in range(hl):
        if input_string[i] != input_string[l - 1 - i]:
            return False
    return True