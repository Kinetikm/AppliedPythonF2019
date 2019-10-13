#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import os


def calc_file_word_count(file, path_to_dir, queue_for_result):
    with open(path_to_dir+'/'+file, encoding='utf-8') as f:
        num = len(f.read().split())
        queue_for_result.put({file: num})


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
    dir_files = [f for f in os.listdir(path_to_dir)]
    queue_for_result = Queue()

    processes = []
    for file in dir_files:
        proc = Process(target=calc_file_word_count, args=(file, path_to_dir, queue_for_result))
        processes.append(proc)
        proc.start()

    for p in processes:
        p.join()

    result = {}

    total = 0

    while not queue_for_result.empty():
        info = queue_for_result.get()
        for file, count in info.items():
            result[file] = count
            total += count
    result['total'] = total

    return result
