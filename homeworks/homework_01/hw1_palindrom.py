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
    l1 = list(input_string)
    l1.reverse()
    if l1 == list(input_string):
        return True
    else:
        return False
