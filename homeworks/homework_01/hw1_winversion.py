#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    input_lst = input_lst[len(input_lst)-1::-1]
    j = 0
    for i in range(len(input_lst)+1):
        if i == len(input_lst) or input_lst[i] == " ":
            if j == 0:
                input_lst[j:i:1] = input_lst[i-1::-1]
            else:
                input_lst[j:i:1] = input_lst[i-1:j-1:-1]
            j = i+1

    return input_lst

