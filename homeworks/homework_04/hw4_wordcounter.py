#!/usr/bin/env python
# coding: utf-8

from multiprocessing import queues, managers, process, Manager, Pool
import os


def func(filename, path_to_dir):
    with open(path_to_dir + '/' + filename, 'r', encoding='utf-8') as fin:
        words = fin.read().split()
        count = len(words)
    return count


def producer(filename, queue, path_to_dir):
    count = func(filename, path_to_dir)
    queue.put((filename, count))


def consumer(queue):
    outputdict = dict()
    total = 0
    while True:
        res = queue.get()
        if res == 'kill':
            break
        total += res[1]
        outputdict[res[0]] = res[1]
        outputdict['total'] = total
    return outputdict


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
    procceses_count = 4
    pool = Pool(procceses_count)
    queue = Manager().Queue()
    files = os.listdir(path_to_dir)

    result = pool.apply_async(consumer, (queue,))

    processes = []

    for file in files:
        proc = pool.apply_async(producer, (file, queue, path_to_dir))
        processes.append(proc)

    for proc in processes:
        proc.get()
    queue.put('kill')
    pool.close()
    pool.join()
    return result.get()
