#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    last_escape = -1
    for i, c in enumerate(input_lst):
        if c == ' ':
            length = i - last_escape - 1
            for j in range(length // 2):
                input_lst[last_escape + 1 + j], input_lst[i - 1 - j] = input_lst[i - 1 - j], input_lst[
                    last_escape + 1 + j]
            last_escape = i
    i = len(input_lst)
    length = i - last_escape - 1
    for j in range(length // 2):
        input_lst[last_escape + 1 + j], input_lst[i - 1 - j] = input_lst[i - 1 - j], input_lst[last_escape + 1 + j]
    return input_lst
