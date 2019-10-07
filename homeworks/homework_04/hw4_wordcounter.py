#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
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
    manager = Manager()
    result = manager.dict()
    files = os.listdir(path_to_dir)
    jobs = []
    for file in files:
        job = Process(target=worker, args=(path_to_dir, file, result))
        jobs.append(job)
        job.start()
    for job in jobs:
        job.join()
    result['total'] = sum(result.values())
    return result

def worker(path_to_dir, file, result):
    with open(path_to_dir + '/' + file) as f:
        count = 0
        for line in f.readlines():
            count += len(line.split())
        result[file] = count
