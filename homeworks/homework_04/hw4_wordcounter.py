#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue
import os


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
    q = Queue()
    words = Manager().dict()
    tasks = []
    for file in os.listdir(path_to_dir):
        q.put(path_to_dir+'/'+file)
    for _ in range(2):
        task = Process(target=f, args=(q, words))
        tasks.append(task)
        task.start()
    for task in tasks:
        task.join()
    words['total'] = sum(words.values())
    return words


def f(queue_of_files, words_in_file):
    while True:
        item = queue_of_files.get_nowait()
        if item is not None:
            with open(item, 'r') as f_id:
                words_in_file[item.split('/')[-1]] = len(f_id.read().split())
        else:
            break
