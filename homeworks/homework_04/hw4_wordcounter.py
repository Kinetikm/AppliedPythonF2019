#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


def count_words(file, path):
    with open(path + '/' + file) as f:
        return len(f.read().split())


def queue_put(q, file, path):
    q.put((file, count_words(file, path)))


def fill_dict(q, res):
    while True:
        file_and_count = q.get()
        if file_and_count == 'end':
            return
        res[file_and_count[0]] = file_and_count[1]
        res['total'] += file_and_count[1]


def word_count_inference(path_to_dir):
    """
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    """
    all_files = os.listdir(path_to_dir)
    if os.cpu_count() < len(all_files):
        proc_num = os.cpu_count()
    else:
        proc_num = len(all_files)

    manager = Manager()
    queue = manager.Queue()
    pool = Pool(proc_num)
    res = manager.dict()
    res['total'] = 0

    pool.apply_async(fill_dict, (queue, res))

    jobs = []
    for file in all_files:
        job = pool.apply_async(queue_put, (queue, file, path_to_dir))
        jobs.append(job)

    for job in jobs:
        job.get()

    queue.put('end')
    pool.close()
    pool.join()
    return res
