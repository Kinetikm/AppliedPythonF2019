#!/usr/bin/env python
# coding: utf-8

from queue import Queue
from multiprocessing import Process
import os


def word_counter(directory, file, dic):
    path = directory + '/' + file
    with open(path, "r", encoding="utf-8") as f:
        words = 0
        for i in f:
            words += len(i.split())
        f.close()
    dic[file] = words
    dic['total'] += words


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
    d = {'total': 0}
    all_processes = Queue()
    all_files = os.listdir(path_to_dir)
    for file in all_files:
        process = Process(target=word_counter(path_to_dir, file, d))
        all_processes.put(process)
        process.start()
    while not all_processes.empty():
        all_processes.get().join()
    return d

