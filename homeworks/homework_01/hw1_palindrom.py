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
    
    len_str = len(input_string) - 1
    
    for counter in range(len(input_string)//2):
        if input_string[counter] != input_string[len_str - counter]:
            return False

    return True

    raise NotImplementedError
