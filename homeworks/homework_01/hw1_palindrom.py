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
    flag = True
    ln = len(input_string) // 2
    for i in range(ln):
        if input_string[i] != input_string[len(input_string) - i - 1]:
            flag = False
    return flag
