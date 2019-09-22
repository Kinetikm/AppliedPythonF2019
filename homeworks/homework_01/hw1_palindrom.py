#!/usr/bin/env python
# coding: utf-8


def check_palindrom(input_string):
	
    if (input_string == input_string[::-1]):
        return True
    else:
        return False
    '''
    Метод проверяющий строку на то, является ли
    она палиндромом.
    :param input_string: строка
    :return: True, если строка являестя палиндромом
    False иначе
    '''    
