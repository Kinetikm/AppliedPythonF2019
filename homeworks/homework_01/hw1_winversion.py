#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    k = 0
    for i in range(len(input_lst)):
        if input_lst[i] == ' ' or i == len(input_lst)-1:
            if i == len(input_lst)-1:
                for j in range(k, k+(i-k+1)//2):
                    input_lst[j], input_lst[k + i - j] = input_lst[k + i - j], input_lst[j]
            else:
                for j in range(k, k+(i-k+1)//2):
                    input_lst[j], input_lst[k+i-j - 1] = input_lst[k+i-j - 1], input_lst[j]
                k = i+1
    return input_lst
    raise NotImplementedError
