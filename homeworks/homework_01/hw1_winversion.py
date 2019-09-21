#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace
    (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''

    cword = str()
    lst_len = len(input_lst)
    for idx in range(lst_len):
        char = input_lst.pop(0)
        cword += char
        if char == ' ' or idx == lst_len - 1:
            if idx != lst_len - 1:
                input_lst.append(cword[:-1])
            else:
                input_lst.append(cword)
            cword = str()

    input_lst.reverse()
    for idx in range(len(input_lst)):
        cword = input_lst.pop(0)
        for char in cword:
            input_lst.append(char)
        input_lst.append(' ')
    if input_lst != []:
        input_lst.pop()
    return input_lst
