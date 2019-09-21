#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    i = 0
    k = 0
    while i <= len(input_lst):
        if input_lst[i] is " ":
            input_lst[k:i:] = input_lst[k:i:][::-1]
            k = i + 1
    input_lst[k::] = input_lst[k::][::-1]
    input_lst = input_lst[::-1]        
    return input_lst

    
