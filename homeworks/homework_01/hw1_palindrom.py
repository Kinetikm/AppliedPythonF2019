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
    a = input_string
    a = list(a)
    flag = 1
    for i in range(int(len(a)/2)):
        if a[i] != a[len(a)-i-1]:
            flag = 0

    if flag:
        return True
    else:
        return False
