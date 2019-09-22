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
    ret_val = True
    for i in range(len(input_string) // 2):
        if input_string[i] != input_string[len(input_string) - 1 - i]:
            ret_val = ret_val & False
            break
    return ret_val
