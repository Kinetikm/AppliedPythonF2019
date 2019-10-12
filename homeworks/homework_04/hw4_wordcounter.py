#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os
import time

PROCESSES_COUNT = 4


def producer_func(path, to_process, queue):
    with open(path + to_process, 'r') as f:
        res = len(f.read().split())
        queue.put((to_process, res))
    time.sleep(1)


def consumer_func(queue):
    data = dict()
    tot = 0
    while True:
        res = queue.get()
        if res == 'kill':
            break
        tot += res[1]
        data[res[0]] = res[1]
    data['total'] = tot
    return data


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
    to_process_list = os.listdir(path_to_dir)
    res = pool.apply_async(consumer_func, (queue, ))
    jobs = []
    for to_process in to_process_list:
        job = pool.apply_async(producer_func, (path_to_dir + '/', to_process, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('kill')
    pool.close()
    pool.join()
    return res.get()
