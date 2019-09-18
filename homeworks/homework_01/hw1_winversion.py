#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    cnt = 0
    for idx in range(0, len(input_lst)):
        if input_lst[-1] == ' ':
            input_lst.pop()
            input_lst.insert(idx, ' ')
            cnt = idx + 1
        else:
            input_lst.insert(cnt, input_lst.pop())
    return input_lst


if __name__ == '__main__':
    input_str = ['e','t',' ', 'i','v', ' ', 'p', 'r']
    print(word_inversion(input_str))
