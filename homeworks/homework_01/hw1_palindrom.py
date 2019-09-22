#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
    if len(input_string) % 2 == 0:
        x = input_string[:len(input_string) // 2]
        y = input_string[len(input_string) // 2:]
        y = y[::-1]
    else:
        x = input_string[:len(input_string) // 2 + 1]
        y = input_string[len(input_string) // 2:]
        y = y[::-1]
    print(x == y)
    '''
    Метод проверяющий строку на то, является ли
    она палиндромом.
    :param input_string: строка
    :return: True, если строка являестя палиндромом
    False иначе
    '''
    raise NotImplementedError
