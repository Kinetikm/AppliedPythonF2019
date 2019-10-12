#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os


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

    files = [f for f in os.listdir(path_to_dir)
             if os.path.isfile(os.path.join(path_to_dir, f))]
    print(files)
    process_count = 8
    queue = Manager().Queue()
    proc_pool = Pool(process_count)
    summary = proc_pool.apply_async(calculate_total, (queue,))

    file_workers = []
    for file in files:
        worker = proc_pool.apply_async(calculate_in_file, (path_to_dir, file, queue))
        file_workers.append(worker)
    for worker in file_workers:
        worker.get()
    queue.put("end")

    retval = summary.get()
    proc_pool.close()
    proc_pool.join()
    return retval


def calculate_in_file(path_to_dir, filename, q):
    cnt = 0
    with open(os.path.join(path_to_dir, filename), 'r') as f:
        for line in f:
            cnt += len(line.strip().split())
    q.put((filename, cnt))


def calculate_total(q):
    d = {"total": 0}
    while True:
        val = q.get()
        if val == "end":
            break
        d[val[0]] = val[1]
        d["total"] += val[1]
    return d
