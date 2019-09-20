#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace
    (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    def inplace_reverse_subarr(arr, left, right):
        temp = 0
        for i in range(int((right - left) / 2)):
            temp = arr[right - 1 - i]
            arr[right - 1 - i] = arr[left + i]
            arr[left + i] = temp

    def find_and_reverse_words(arr):
        start = False if len(arr) > 0 and arr[0] == ' ' else True
        offset = 0
        for i in range(len(arr)):
            if start and arr[i] == ' ':
                start = False
                inplace_reverse_subarr(arr, offset, i)
                offset = i + 1
            elif not start:
                if arr[i] == ' ':
                    offset += 1
                else:
                    start = True
        if start:
            inplace_reverse_subarr(arr, offset, len(arr))
    inplace_reverse_subarr(input_lst, 0, len(input_lst))
    find_and_reverse_words(input_lst)
    return input_lst
