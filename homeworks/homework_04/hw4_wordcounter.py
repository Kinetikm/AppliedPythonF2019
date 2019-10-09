#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os

processes_avaliable = os.cpu_count()

def consumer_func(queue):
    dict = {"total":0}
    while True:
        val = queue.get()
        if val == "This is the end)":
            return dict
        else:
            dict[val[0].split('/')[-1]] = val[1]
            dict["total"] += val[1]

def words_counter(file, queue):
    with open(file) as f:
        res = len(f.read().strip().split())
        queue.put((file, res))

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
    pool = Pool(processes_avaliable)
    res = pool.apply_async(consumer_func, (queue, ))
    jobs = []
    for file in os.listdir(path_to_dir):
        j = pool.apply_async(words_counter, args=(path_to_dir + '/' + file, queue))
        jobs.append(j)
    for j in jobs:
        j.get()
    queue.put("This is the end)")
    pool.close()
    pool.join()
    return res
