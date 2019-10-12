#!/usr/bin/env python
# coding: utf-8

import multiprocessing
from multiprocessing import Process, Manager
import os


def count_words(short_fname="", queue: multiprocessing.Queue=None, full_name=""):
    wcount = 0

    with open(full_name, "r") as f:
        for line in f:
            wcount += len([None for w in line.strip().split(" ") if len(w) > 0])

    queue.put((short_fname, wcount))
    return


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

    result = dict()
    proc_list = []
    manager = Manager()
    queue = manager.Queue()
    for f in os.listdir(path_to_dir):
        full_fname = os.path.join(path_to_dir, f)
        if not os.path.isfile(full_fname):
            continue

        proc = Process(target=count_words, kwargs=dict(queue=queue, full_name=full_fname, short_fname=f))
        proc_list.append(proc)
        proc.start()

    for p in proc_list:
        wcount = queue.get()
        result[wcount[0]] = wcount[1]

    for p in proc_list:
        p.join()

    if 'total' in result:
        raise Exception("В задании не было такого кейса")

    result['total'] = sum(result.values())
    print(result)
    return result
