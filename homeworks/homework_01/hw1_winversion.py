#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    begin = 0
    end = 0
    for end in range(len(input_lst)):
        if input_lst[end] == ' ':
            if end == 0:
                continue
            if begin == 0:
                input_lst[:end] = input_lst[end - 1::-1]
            else:
                input_lst[begin-1:end] = input_lst[end:begin-1:-1]
            begin = end + 1
    if (begin == 0):
        input_lst.reverse()
    else:
        input_lst[begin:] = input_lst[end:begin - 1:-1]
    return input_lst
