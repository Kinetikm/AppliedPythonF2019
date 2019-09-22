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
    mas = []
    for i in range(len(input_string)):
        mas.append(input_string[i])
    mas.reverse()
    for i in range(len((input_string))):
        if mas[i] != input_string[i]:
            return False
    return True
