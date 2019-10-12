#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Pool
from functools import reduce
import os


def word_counts(line):
    return reduce(lambda counts, _: counts + 1,
                  (filter(lambda word: True if word not in {"", "\n", "\t"} else False,
                          line.split(" "))), 0)


def word_counts_in_file(file):
    with open(file) as f:
        counts = reduce(lambda counts, line: counts + word_counts(line),
                        f, 0)
    return counts


def word_count_inference(path_to_dir):
    '''
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    '''
    files = os.listdir(path_to_dir)
    pool = Pool(os.cpu_count())  # Всё моё !!!
    res = pool.map(word_counts_in_file,
                   map(lambda file: os.path.join(path_to_dir, file),
                       files)
                   )

    total = 0
    _dict = {}
    for key, value in zip(files, res):
        _dict[key] = value
        total += value
    _dict["total"] = total
    return _dict
