#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Queue, Manager, Pool
import os


def num_words(dir, fname, queue):
    words = 0
    with open(dir + '/' + fname, 'r') as file:
        for line in file:
            words += len(line.split())
    queue.put((fname, words))


def consumer_func(queue, result_dct):
    while True:
        res = queue.get()
        if res == 'kill':
            break
        result_dct[res[0]] = res[1]
        result_dct['total'] += res[1]


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
    PROCESSES_COUNT = 5
    file_lst = os.listdir(path=path_to_dir)
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)
    result_dct = manager.dict()
    result_dct['total'] = 0
    pool.apply_async(consumer_func, (queue, result_dct))
    jobs = []
    for file in file_lst:
        job = pool.apply_async(num_words, (path_to_dir, file, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('kill')
    pool.close()
    pool.join()
    return result_dct
