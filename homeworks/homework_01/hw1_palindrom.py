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
    input_string = input_string.lower()
    for l in input_string:
        if (ord("a") <= ord(l) <= ord("z")):
            continue
        else:
            input_string = input_string.replace(l, "")
    if input_string == input_string[::-1]:
        return True
    else:
        return False
