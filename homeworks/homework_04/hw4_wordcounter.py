#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


def producer_func(file_, path_to_dir, queue):
    try:
        with open(os.path.join(path_to_dir, file_), 'r') as f:
            ctr = 0
            for line in f:
                for word in line.strip().split():
                    ctr += 1
        queue.put({file_: ctr})
    except IsADirectoryError:
        pass


def consumer_func(queue):
    res_dict = {}
    total = 0
    while True:
        new_val = queue.get()
        if new_val == 'stop iteration':
            break
        for value in new_val.values():
            total += value
        res_dict.update(new_val)
    res_dict['total'] = total
    return res_dict


def word_count_inference(path_to_dir, process_num=4):
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
    pool = Pool(process_num)
    files = os.listdir(path_to_dir)
    cons_job = pool.apply_async(consumer_func, (queue,))
    jobs = []
    for file_ in files:
        job = pool.apply_async(producer_func, (file_, path_to_dir, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('stop iteration')
    result = cons_job.get()
    pool.close()
    return result
