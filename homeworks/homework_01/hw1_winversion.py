#!/usr/bin/env python
# coding: utf-8


def reverse(start_pos, end_pos, lst):
    for i in range((end_pos - start_pos + 1) // 2):
        lst[i + start_pos], lst[end_pos - i] = lst[end_pos - i], lst[i + start_pos]


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    if ' ' not in input_lst:
        return input_lst
    start_pos = 0
    input_lst.reverse()
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            reverse(start_pos, i - 1, input_lst)
            start_pos = i + 1
    reverse(start_pos, i, input_lst)
    return input_lst
