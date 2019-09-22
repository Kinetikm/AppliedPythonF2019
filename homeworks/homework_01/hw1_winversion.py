#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    input_lst.reverse()
    left = 0
    k = 0
    for i in range(len(input_lst)):
        if ((input_lst[i] == ' ') or (i + 1 == len(input_lst))):
            if (i + 1 == len(input_lst)):
                right = i
            else:
                right = i - 1
            while (right - k > left + k):
                temp = input_lst[left + k]
                input_lst[left + k] = input_lst[right - k]
                input_lst[right - k] = temp
                k += 1
            k = 0
            left = i + 1
    return (input_lst)
