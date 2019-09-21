#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    sentence = input_lst[::-1]
    w_start = 0
    for i in range(len(sentence)):
        if sentence[i] == ' ':
            sentence[w_start:i] = (sentence[w_start:i])[::-1]
            w_start = i + 1
    sentence[w_start:] = (sentence[w_start:])[::-1]
    return sentence
