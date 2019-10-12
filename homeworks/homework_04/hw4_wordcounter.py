#!/usr/bin/env python
# coding: utf-8

import multiprocessing
from multiprocessing import Process, Manager, Pool, Queue
import os


MAX_PROCS = 10


def count_words_in_file(full_name):
    wcount = 0

    with open(full_name, "r") as f:
        for line in f:
            wcount += len([None for w in line.strip().split(" ") if len(w) > 0])
    return wcount


def count_words_worker(files_queue: multiprocessing.Queue, word_count_queue: multiprocessing.Queue):

    # print("running worker", os.getpid())
    for short_fname, full_name in iter(files_queue.get, 'STOP'):
        wcount = count_words_in_file(full_name)
        word_count_queue.put((short_fname, wcount))

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

    with Manager() as manager:
        with Pool(processes=MAX_PROCS) as pool:

            files_queue = manager.Queue()
            word_count_queue = manager.Queue()
            # print("running poll")

            for i in range(MAX_PROCS):
                pool.apply_async(count_words_worker, (files_queue, word_count_queue))

            total_files = 0
            for f in os.listdir(path_to_dir):

                full_fname = os.path.join(path_to_dir, f)
                if not os.path.isfile(full_fname):
                    continue

                total_files += 1
                # print("put in queue", f)
                files_queue.put((f, full_fname))

            for p in range(total_files):
                # print("getting results")
                short_fname, wcount = word_count_queue.get()
                result[short_fname] = wcount

            for i in range(MAX_PROCS):
                files_queue.put('STOP')

            pool.close()
            pool.join()

            if 'total' in result:
                raise Exception("В задании не было такого кейса")

    result['total'] = sum(result.values())
    # print(result)
    return result
