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

    for i in range(len(input_string) // 2):
        if input_string[i].lower() != input_string[len(input_string) - i - 1]:
            return False

    return True
