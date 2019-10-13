#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def count_file_words(filename, dirname, output):
    word_counter = 0
    with open("{}/{}".format(dirname, filename)) as file:
        for line in file:
            word_counter += len(line.split())
        file.close()
    output[filename] = word_counter
    output["total"] += word_counter


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
    output = Manager().dict()
    procs = []
    output["total"] = 0
    queue = Manager().Queue()
    for file in os.listdir(path_to_dir):
        queue.put(file)
    max_procs = 10
    while not queue.empty():
        for proc in procs:
            if not proc.is_alive():
                proc.terminate()
                procs.remove(proc)
        for i in range(min(max_procs-len(procs), queue.qsize())):
            proc = Process(target=count_file_words, args=(queue.get(), path_to_dir, output))
            procs.append(proc)
            proc.start()
    for proc in procs:
        proc.join()
    return output
