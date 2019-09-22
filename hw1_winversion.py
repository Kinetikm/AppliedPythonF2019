#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    
    input_lst = input_lst[::-1]
    i = 0
    k = 0
    while i < len(input_lst):
        if input_lst[i] == " ":
            input_lst = input_lst[i-1::-1] + input_lst[i:]
            k = i
            i += 1
            break
        i += 1

    while i < len(input_lst):
        if input_lst[i] == " ":    
            input_lst = input_lst[:k+1] + input_lst[i-1:k:-1] + input_lst[i:]
            k = i
        i += 1
    
    if k == 0:
        input_lst = input_lst[::-1]
        return input_lst

    if input_lst[i-1] != " ":
        input_lst = input_lst[:k+1] + input_lst[i-1:k:-1]

    return input_lst
    # raise NotImplementedError