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
    length = len(input_string)
    length = length//2
    for i in range(length):
        if input_string[i] != input_string[-1-i]:
            return False
            break
    return True

