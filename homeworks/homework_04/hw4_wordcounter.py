#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


PROCESS_COUNT = 5


def file_proccessing(filename, queue):
    with open(filename, 'r') as f:
        data = f.read()
        data = data.split()
        queue.put((filename, len(data)))


def word_counter(queue):
    result = {}
    while True:
        res = queue.get()
        if res is None:
            result['total'] = sum(result.values())
            return result
        filename, count = res
        result[filename.split('/')[-1]] = count


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
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(PROCESS_COUNT)

    res = pool.apply_async(word_counter, (queue,))

    jobs = []
    for file in os.listdir(path_to_dir):
        job = pool.apply_async(file_proccessing, (path_to_dir + '/' + file, queue,))
        jobs.append(job)

    for job in jobs:
        job.get()

    queue.put(None)
    pool.close()
    pool.join()

    return res.get()
