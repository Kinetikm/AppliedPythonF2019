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
    new_input_string = [input_string[i] for i in range(len(input_string))] #if input_string[i] != ' 'py
    for i in range(len(new_input_string) // 2):
        if new_input_string[-1-i] != new_input_string[i]:
            return(False)
    else:
        return(True)


