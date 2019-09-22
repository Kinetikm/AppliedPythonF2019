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
    left = 0
    right = len(input_string) - 1
    k = 0
    if input_string == '':
        return False
    else:
        if input_string == input_string[::-1]:
            return True
        else:
            return False
