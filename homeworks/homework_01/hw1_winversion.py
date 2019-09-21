#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param  input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    try:
        ind = input_lst.index(' ')
    except ValueError:
        return input_lst
    next_ind = ind

    # Execute all words except for the last one
    while True:
        try:
            next_ind += input_lst[ind + 1::].index(' ') + 1
        except ValueError:
            break
        for _ in range(next_ind, ind, -1):
            input_lst.insert(0, input_lst.pop(next_ind))
        ind = next_ind

    # Remove the last word to beginning
    ind = 0
    for item in input_lst[-1::-1]:
        if item != ' ':
            input_lst.insert(0, input_lst.pop(len(input_lst) - 1))
            ind += 1
        else:
            input_lst.insert(ind, input_lst.pop(len(input_lst) - 1))
            break
    return input_lst

