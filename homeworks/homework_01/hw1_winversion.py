#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    i0 = 0
    try:
        input_lst.index(' ')
    except ValueError:
        return None
    for i in range(len(input_lst)):
        if input_lst[i] == ' ':
            k = (i - i0 + 1) // 2
            for j in range(k):
                input_lst[i] = input_lst[i0 + j]
                input_lst[i0 + j] = input_lst[i - j - 1]
                input_lst[i - j - 1] = input_lst[i]
            input_lst[i] = ' '
            i0 = i + 1
    if input_lst[i0 - 1] == ' ':
        k = (len((input_lst)) - i0 + 1) // 2
        for j in range(k):
            input_lst[i0 - 1] = input_lst[len(input_lst) - 1 - j]
            input_lst[len(input_lst) - 1 - j] = input_lst[i0 + j]
            input_lst[i0 + j] = input_lst[i0 - 1]
        input_lst[i0 - 1] = ' '
        input_lst[::] = input_lst[::-1]
    return input_lst
