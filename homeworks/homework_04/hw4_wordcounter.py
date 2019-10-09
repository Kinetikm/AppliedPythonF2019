#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


PROCESSES_COUNT = os.cpu_count()


def file_word_count(path, filename, queue):
    count = 0
    with open(path + '/' + filename, 'r') as f:
        for line in f:
            count += len(line.split())
    item = {filename: count}
    queue.put(item)


def consumer_func(queue):
    words_dict = {'total': 0}
    while True:
        res = queue.get()
        if res == '*kill*':
            break
        words_dict.update(res)
    words_dict['total'] = sum(words_dict.values())
    return words_dict


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
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)

    word_dict = pool.apply_async(consumer_func, (queue,))
    jobs = []
    for file in os.listdir(path_to_dir):
        if os.path.isfile(path_to_dir + '/' + file):
            job = pool.apply_async(file_word_count, (path_to_dir, file, queue,))
            jobs.append(job)

    for job in jobs:
        job.get()

    queue.put('*kill*')
    pool.close()
    pool.join()

    return word_dict.get()
