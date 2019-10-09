#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Manager, Pool
import os


N_WORKERS = os.cpu_count()


def file_len(fname, path, queue):
    n_words = 0
    with open(os.path.join(path, fname)) as f:
        for line in f:
            words = line.split()
            n_words += len(words)
    queue.put((fname, n_words))


def collector(queue):
    total = 0
    result = {}
    while True:
        element = queue.get()
        if element == 'END_QUEUE':
            break
        result[element[0]] = element[1]
        total += element[1]
    result['total'] = total
    return result


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
    files_list = [i for i in os.listdir(path_to_dir) if os.path.isfile(os.path.join(path_to_dir, i))]
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(N_WORKERS)
    task = pool.apply_async(collector, (queue,))
    jobs = []
    for f in files_list:
        job = pool.apply_async(file_len, (f, path_to_dir, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('END_QUEUE')
    result = task.get()
    pool.close()
    pool.join()
    return result
