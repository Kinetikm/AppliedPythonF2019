#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def num_words(dir, fname, result):
    words = 0
    for line in open(dir).readlines():
        words += len(line.split())
    result[fname] = words


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

    total = 0
    manager = Manager()
    result = manager.dict()
    tasks = []
    lst_of_f = os.listdir(path=path_to_dir)
    for i in lst_of_f:
        task = Process(target=num_words, args=(path_to_dir + '/' + i, i, result))
        tasks.append(task)
        task.start()
    for task in tasks:
        task.join()
    for value in result.values():
        total += value
    result['total'] = total
    return result
