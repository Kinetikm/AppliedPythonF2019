#!/usr/bin/env python
# coding: utf-8


def append(input_lst, space_pos, start_pos):
    input_lst.append(' ')
    input_lst = input_lst[:start_pos:] + input_lst[space_pos+1::] + input_lst[start_pos:space_pos:]
    return input_lst, (len(input_lst) - space_pos)


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    start_pos = 0
    try:
        space_pos = len(input_lst)-input_lst[::-1].index(' ')-1
    except ValueError:
        return input_lst
    while start_pos < space_pos:
        input_lst, temp = append(input_lst, space_pos, start_pos)
        start_pos += temp
        space_pos = len(input_lst)-input_lst[::-1].index(' ')-1
    return input_lst
