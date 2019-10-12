#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def word_count(queue, dict_f, path_to_dir):
    fn = queue.get()
    with open(path_to_dir + '/' + fn) as f:
        dict_f[fn] = len(f.read().split())
        print(fn, dict_f)


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
    files_list = os.listdir(path_to_dir)
    f_num = len(files_list)
    manager = Manager()
    q = manager.Queue()
    dict_f = manager.dict()

    for fname in files_list:
        q.put(fname)

    proc_list = []
    for i in range(f_num):
        proc = Process(target=word_count, args=(q, dict_f, path_to_dir, ))
        proc_list.append(proc)
        proc.start()

    for p in proc_list:
        p.join()

    dict_f['total'] = sum(dict_f.values())

    return dict_f
