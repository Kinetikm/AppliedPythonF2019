#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Pool, Manager
import os


def word_count(path_to_dir, filename, queue):
    words = 0
    with open("{}/{}".format(path_to_dir, filename), 'r') as f:
        for line in f:
            wordslist = line.split()
            words += len(wordslist)
    item = {filename: words}
    queue.put(item)


def consumer_func(queue):
    words_dict = dict()
    total = 0
    while True:
        elem = queue.get()
        if elem == 'kill':
            break
        words_dict.update(elem)
    for k in words_dict:
        total += words_dict[k]
    words_dict['total'] = total
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
    pool = Pool(os.cpu_count())
    task = pool.apply_async(consumer_func, (queue, ))
    jobs = []
    for filename in os.listdir(path_to_dir):
        job = pool.apply_async(word_count, (path_to_dir, filename, queue))
        jobs.append(job)
    for job in jobs:
        job.get()
    queue.put('kill')
    pool.close()
    pool.join()
    return task.get()
