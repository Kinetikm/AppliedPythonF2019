#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    begin = 0
    n = len(input_lst)
    for i in range(n):
        if input_lst[i] == ' ':
            for j in range((i - begin) // 2):
                input_lst[begin + j], input_lst[i - 1 - j] = input_lst[i - 1 - j], input_lst[begin + j]
            begin = i + 1
    for j in range((n - begin) // 2):
        input_lst[begin + j], input_lst[n - 1 - j] = input_lst[n - 1 - j], input_lst[begin + j]
    input_lst.reverse()
    return input_lst
