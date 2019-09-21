#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    for i in range(len(input_lst) // 2):
        input_lst[-1 - i], input_lst[i] = input_lst[i], input_lst[-1 - i]
    i = 0
    while i < len(input_lst):
        space_num = i
        while space_num < len(input_lst) - 1 and input_lst[space_num] != ' ':
            space_num += 1
        if input_lst[space_num] == ' ':
            space_num -= 1
        for num, k in enumerate(range(i, i + ((space_num - i + 1) // 2))):
            input_lst[space_num - num], input_lst[k] = input_lst[k], input_lst[space_num - num]
        i = space_num + 2
        if space_num + 1 == len(input_lst):
            break
        if input_lst[space_num + 1] != ' ':
            break
    return input_lst
