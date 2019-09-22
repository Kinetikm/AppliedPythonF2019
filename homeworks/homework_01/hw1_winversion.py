#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    n = input_lst.count(' ')
    input_lst.reverse()
    print(input_lst)
    start = 0
    for i in range(n + 1):
        if i < n:
            end = input_lst.index(' ') - 1
            input_lst[input_lst.index(' ')] = '.'
        else:
            end = len(input_lst) - 1
        for i in range((end - start + 1) // 2):
            c = input_lst[start + i]
            input_lst[start + i] = input_lst[end - i]
            input_lst[end - i] = c
        start = end + 2
    for i in range(len(input_lst)):
        if input_lst[i] == '.':
            input_lst[i] = ' '
    return input_lst
