#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue
from os import listdir, path
from os.path import isfile, join


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
    result = {}
    allProcesses = []
    queue = Queue()
    for filename in listdir(path_to_dir):
        proc = Process(target=file_word_count, args=(path.join( path_to_dir, filename), queue))
        allProcesses.append(proc)
        proc.start()
    total = 0

    for _ in listdir(path_to_dir):
        file_proc_res = queue.get()
        result[file_proc_res[0]] = file_proc_res[1]
        total += file_proc_res[1]

    result['total'] = total
    return result


def file_word_count(filename, queue):
    with open(filename, 'r') as file:
        text =  file.read().rstrip(' ').split()
        queue.put([filename.split('/')[-1], len(text)])

        