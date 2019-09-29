#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    """"
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    """
    if ' ' not in input_lst:
        return input_lst
    list_size = len(input_lst)
    for i in range(list_size//2):
        input_lst[i], input_lst[list_size - i - 1] = input_lst[list_size - i - 1], input_lst[i]
    word_start = 0
    for i in range(list_size):
        if input_lst[i] == ' ':
            word_size = i - word_start
            for j in range(word_size // 2):
                input_lst[word_start + j], input_lst[i - j - 1] = input_lst[i - j - 1],\
                                                                  input_lst[word_start + j]
            word_start = i + 1
    for k in range((list_size - word_start)//2):
        input_lst[word_start + k], input_lst[list_size - k - 1] = input_lst[list_size - k - 1],\
                                                                  input_lst[word_start + k]
    return input_lst
