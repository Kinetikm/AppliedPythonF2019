#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager
import os


PROCESSES_COUNT = os.cpu_count()


def worker(queue, shared_dict):
    while True:
        res = queue.get()
        if res == -1:
            break

        counter = 0
        with open(res, 'r') as f:
            for line in f:
                counter += len(line.split())
        print(res, counter)

        shared_dict[res.split('/')[-1]] = counter
        shared_dict['total'] += counter


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
    shared_dict = manager.dict()
    shared_dict['total'] = 0

    pool.apply_async(worker, (queue, shared_dict))

    for filename in os.listdir(path_to_dir):
        queue.put(path_to_dir + '/' + filename)

    queue.put(-1)
    pool.close()
    pool.join()

    return shared_dict
