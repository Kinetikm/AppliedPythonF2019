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
    for ind, val in enumerate(input_string):
        if val != input_string[-1-ind]:
            return False
        if ind == length // 2:
            break
    return True


    # raise NotImplementedError
