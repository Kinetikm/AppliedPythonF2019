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
    i = 0
    flag = True
    while i < len(input_string)//2:
        if input_string[i] != input_string[len(input_string)-1-i]:
            flag = False
            break
        else:
            i = i + 1
    return flag
