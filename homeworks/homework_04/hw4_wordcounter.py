#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def word_counter(path_to_file, filename, out_dict):
    out = 0
    with open("{}/{}".format(path_to_file, filename)) as file:
        for line in file:
            out += len(line.split())
        file.close()
    out_dict[filename] = out
    out_dict["total"] += out


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
    out, out["total"] = manager.dict(), 0
    ps = []
    for file in os.listdir(path_to_dir):
        p = Process(target=word_counter(path_to_dir, file, out))
        ps.append(p)
        p.start()
    for p in ps:
        p.join()
    return out
