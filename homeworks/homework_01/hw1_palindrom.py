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
    raise NotImplementedError
    i = 0
    flag = True
    while i < len(a)//2:
    if a[i] != a[len(a)-1-i]:
        flag = False
        break
    else:
        i = i + 1
    return flag
