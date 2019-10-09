#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Pool, Manager, Queue
import os


def producer(file_path, queue):
    sum_words = 0
    with open(file_path, 'r') as f:
        sum_words = len(f.read().strip().split())
        queue.put((file_path.split('/')[-1], sum_words))


def consumer(queue):
    dict_ = {}
    total = 0
    while True:
        result = queue.get()
        if result == 'kill':
            break
        dict_[result[0]] = result[1]
        total += result[1]
    dict_['total'] = total
    return dict_


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
    PROCESSES_COUNT = 4
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESSES_COUNT)
    list_files = os.listdir(path_to_dir)

    cons = pool.apply_async(consumer, (queue, ))
    jobs = []
    for file in list_files:
        job = pool.apply_async(producer, (path_to_dir + '/' + file, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('kill')
    res = cons.get()
    pool.close()
    pool.join()
    return res
