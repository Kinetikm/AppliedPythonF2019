#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    dop_str = input_lst[::-1]
    output_str = []
    fout = 0
    for i in range(len(dop_str)):
        if dop_str[i] == ' ':
            word = (dop_str[fout:i])[::-1]
            for l in range(len(word)):
                output_str.append(word[l])
            fout = i + 1
            output_str.append(" ")
    else:
        word = (dop_str[fout:len(input_lst)])[::-1]
        for l in range(len(word)):
            output_str.append(word[l])
    return output_str