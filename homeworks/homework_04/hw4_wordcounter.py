#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


def num_of_words(filename):
    with open(filename, 'r') as f:
        return len(f.read().split())


def producer_func(path_to_dir, filename, queue):
    res = (filename, num_of_words(path_to_dir + '/' + filename))
    queue.put(res)


def consumer_func(queue):
    dict_ = {'total': 0}
    while True:
        res = queue.get()
        if res == 'kill':
            return dict_
        dict_[res[0]] = res[1]
        dict_['total'] += res[1]


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
    file_names = os.listdir(path_to_dir)
    PROCESSES_COUNT = len(file_names)

    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)

    cons = pool.apply_async(consumer_func, (queue, ))

    jobs = []
    for filename in file_names:
        job = pool.apply_async(producer_func, (path_to_dir, filename, queue))
        jobs.append(job)
    for job in jobs:
        job.get()

    queue.put('kill')
    pool.close()
    pool.join()

    return cons.get()
