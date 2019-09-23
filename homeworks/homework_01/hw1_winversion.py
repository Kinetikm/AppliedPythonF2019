#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst = input_lst[::-1]
    i = 0
    j = 0
    while i < len(input_lst):
        if input_lst[i] == ' ':
            k = i - 1
            while k >= j:
                input_lst[j], input_lst[k] = input_lst[k], input_lst[j]
                j += 1
                k -= 1
            j = i + 1
        i += 1
    i -= 1
    while i >= j:
        input_lst[i], input_lst[j] = input_lst[j], input_lst[i]
        i -= 1
        j += 1
    return input_lst
