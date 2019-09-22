#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    start = 0
    len_lst = len(input_lst)

    for end in range(len_lst):
        if input_lst[end] == ' ':
            if start == 0:
                input_lst[:end] = input_lst[end - 1::-1]
            else:
                input_lst[start-1:end] = input_lst[end:start-1:-1]

            start = end + 1
    input_lst[start:] = input_lst[end:start - 1:-1]
    return None
