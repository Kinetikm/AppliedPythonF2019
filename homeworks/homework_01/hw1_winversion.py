#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst = input_lst[::-1]
    k = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            input_lst[k:i] = input_lst[k:i:-1]
            k = i+1
    input_lst[k:] = input_lst[k::-1]
    return input_lst
