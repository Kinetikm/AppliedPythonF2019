#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    input_lst.reverse()

    word_start = 0
    for (i, elem) in enumerate(input_lst):
        if elem == ' ':
            input_lst[word_start:i] = input_lst[word_start:i:-1]
            word_start = i + 1

    return input_lst
