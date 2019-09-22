#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    cnt = 0
    for idx in range(len(input_lst)):
        if input_lst[-1] == ' ':
            for idx2 in range(idx, len(input_lst)):
                input_lst[idx2], input_lst[len(input_lst) - 1] = \
                    input_lst[len(input_lst) - 1], input_lst[idx2]
            cnt = idx + 1
        else:
            for idx2 in range(cnt, len(input_lst)):
                input_lst[idx2], input_lst[len(input_lst) - 1] = \
                    input_lst[len(input_lst) - 1], input_lst[idx2]
    return input_lst


if __name__ == '__main__':
    input_str = ['e', 't', ' ', 'i', 'v', ' ', 'p', 'r']
    print(word_inversion(input_str))
