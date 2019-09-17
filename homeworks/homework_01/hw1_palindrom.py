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
    index_middle = int(len(input_string)/2)
    if (len(input_string) % 2 == 0):
        return (input_string[:index_middle][::-1] == input_string[index_middle:])
    else:
        return (input_string[:index_middle][::-1] == input_string[index_middle + 1:])
