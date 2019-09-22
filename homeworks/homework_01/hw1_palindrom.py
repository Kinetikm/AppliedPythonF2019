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
    def palindrome(input_string):
    l = len(input_string)
    for i in range(l//2):
        if input_string[i] != input_string[l - i - 1]:
            return False
    return True
