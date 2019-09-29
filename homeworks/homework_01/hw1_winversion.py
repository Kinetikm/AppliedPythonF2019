#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    input_lst = input_lst[::-1]
    lastcheck = 0
    for i in range(0, len(input_lst)):
        if input_lst[i] == ' ':
            cycl = lastcheck + (i - lastcheck) // 2
            for j in range(lastcheck, cycl):
                input_lst[j], input_lst[i-1-j+lastcheck] = input_lst[i-1-j+lastcheck], input_lst[j]
            lastcheck = i + 1
        if i == (len(input_lst) - 1):
            cycl = lastcheck + (i - lastcheck) // 2
            for j in range(lastcheck, cycl):
                input_lst[j], input_lst[i - j + lastcheck] = input_lst[i - j + lastcheck], input_lst[j]
    return input_lst
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
