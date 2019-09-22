#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
	'''
    l = 0
    r = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            r = i
            input_lst[l:r] = input_lst[l:r][::-1]
            l = i + 1
    input_lst[l:] = input_lst[l:][::-1]
    input_lst = input_lst[::-1]
return input_lst