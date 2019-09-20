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
    x = len(input_string)
    return input_string[:(x // 2)].lower() == input_string[:(x + 1) // 2 - 1:-1].lower()
