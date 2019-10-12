#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


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
    core = os.cpu_count()
    files = [f for f in os.listdir(path_to_dir)
             if os.path.isfile(os.path.join(path_to_dir, f))]
    manager = Manager()
    queue = manager.Queue()
    pool = Pool(core)
    total = pool.apply_async(search_total, (queue, ))
    for file in files:
        process = pool.apply_async(words_in_file, (path_to_dir, file, queue))
        process.get()
    queue.put('END')
    return total.get()


def words_in_file(path_to_dir, filename, queue):
    sum = 0
    with open(os.path.join(path_to_dir, filename), 'r') as file:
        for line in file:
            sum += len(line.strip().split())
    queue.put((filename, sum))


def search_total(queue):
    total = 0
    res = {}
    while True:
        tmp = queue.get()
        if tmp == 'END':
            break
        res[tmp[0]] = tmp[1]
        total += tmp[1]
        res['total'] = total

    return res
