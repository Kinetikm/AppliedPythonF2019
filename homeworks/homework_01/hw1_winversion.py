#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    reverse_lst = input_lst[::-1]
    start_index = 0
    for index in range(len(reverse_lst)):
        if reverse_lst[index] == "\x20":
            end_index = index
            reverse_lst[start_index:end_index] = reverse_lst[start_index:end_index][::-1]
            start_index = index+1
    reverse_lst[start_index:] = reverse_lst[start_index:][::-1]
    return reverse_lst
