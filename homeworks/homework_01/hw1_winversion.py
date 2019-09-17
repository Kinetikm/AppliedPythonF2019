#!/usr/bin/env python
# coding: utf-8


def word_inversion(input_lst):
    '''
    Метод инвертирующий порядок слов в строке inplace (без выделения доп памяти)
    :param input_lst: строка-массив букв (['H', 'i']). Пробелы одиночные
    :return: None Все изменения в input_lst проходят
    '''
    reversed_lst = [letter for letter in ' '.join(''.join(input_lst).split(' ')[::-1])]
    # Следующие две строкиотвечают за inplace:
    [input_lst.pop() for idx in range(0, len(input_lst))]
    input_lst.__iadd__([reversed_lst])
    return input_lst


if __name__ == '__main__':
    str = ['H', 'i', ' ', 'M', 'L']
    print(id(str))
    word_inversion(str)
    print(str, id(str))
