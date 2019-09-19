#!/usr/bin/env python
# coding: utf-8


def rev(A):
    n = len(A)
    for i in range(int(n/2)):
        temp = A[i]
        A[i] = A[n - i - 1]
        A[n - i - 1] = temp
    return A


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    B = input_lst
    B = rev(B)
    l = 0
    r = 0
    for i in range(len(B)):
        if B[i] == ' ':
            r = i
            B[l:r] = rev(B[l:r])
            l = i+1
    B[l:] = rev(B[l:])
    return B
