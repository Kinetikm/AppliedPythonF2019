#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def producer_func(file, queue, path_to_file):
    res = func(file, path_to_file)
    queue.put({file: res})


def consumer_func(queue):
    result = {'total': 0}
    while True:
        res = queue.get()
        if res == 'kill-9':
            queue.put(result)
            break
        a = 0
        for i in res.values():
            a = i
        result.update(res)
        result.update({'total': result['total'] + a})


def func(file, path_to_dir):
    with open(f'{path_to_dir}/{file}', 'r') as f:
        return len(f.read().strip().split())


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
    pool = Pool(os.cpu_count())

    pool.apply_async(consumer_func, args=(queue,))

    to_process_list = os.listdir(path_to_dir)

    jobs = []
    for file in to_process_list:
        job = pool.apply_async(producer_func, args=(file, queue, path_to_dir,))
        jobs.append(job)
    for job in jobs:
        job.get()

    queue.put('kill-9')
    result = queue.get()
    return result
