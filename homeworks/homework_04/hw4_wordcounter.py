#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager
import os


def count_of_words(file, queue):
    with open(file) as f:
        num_of_words = 0
        for line in f:
            num_of_words += len(line.split())
        queue.put((file.split('/')[-1], num_of_words))


def count_all_words(queue):
    dict_of_count = {}
    total = 0
    while True:
        item = queue.get()
        if item == 'kill':
            break
        total += item[1]
        dict_of_count[item[0]] = item[1]
    dict_of_count['total'] = total
    return dict_of_count


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
    num_of_process = len(all_files)
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(num_of_process)
    result = pool.apply_async(count_all_words, (queue,))
    processes = []
    for file_ in all_files:
        process = pool.apply_async(count_of_words, (path_to_dir + '/' + file_, queue))
        processes.append(process)

    for process in processes:
        process.get()

    queue.put('kill')
    pool.close()
    pool.join()
    return result.get()
