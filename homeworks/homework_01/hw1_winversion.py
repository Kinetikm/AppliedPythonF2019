#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_list):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_list: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    c = 0
    for i in range(len(input_list)):
        if (c < len(input_list)) and (input_list[i] == " "):
            input_list[c:i] = input_list[c:i][::-1]
            c = i + 1
    input_list[c:] = input_list[c:][::-1]
    return input_list[::-1]
