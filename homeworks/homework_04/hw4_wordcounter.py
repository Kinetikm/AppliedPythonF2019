#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Pool, Manager
import os


def counter(f_name, q, res):
    with open(f_name, 'r') as f:
        cnt = 0
        for line in f:
            cnt += len(line.split())

        res[f_name.split('/')[-1]] = cnt
        q.put(cnt)


def total_count(q, res):
    total = 0
    while True:
        cnt = q.get()
        if cnt == -1:
            break
        total += cnt

    res['total'] = total
    return dict(res)


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

    files = [path_to_dir + "/" + f for f in os.listdir(path_to_dir)]

    manager = Manager()
    queue = manager.Queue()
    result = manager.dict()
    pool = Pool(len(files) + 1)

    total_proc = pool.apply_async(total_count, (queue, result))

    for file in files:
        proc = pool.apply_async(counter, (file, queue, result))
        proc.get()

    queue.put(-1)
    return total_proc.get()
