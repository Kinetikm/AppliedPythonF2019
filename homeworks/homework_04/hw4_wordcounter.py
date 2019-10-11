#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def count_words(queue, result_dict):
    while not queue.empty():
        item = queue.get()
        try:
            file_path = item[1] + '/' + item[0]
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
                text = text.split()
            result_dict[item[0]] = len(text)
        except Exception:
            pass


def word_count_inference(path_to_dir):
    """
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    """

    data = os.listdir(path_to_dir)
    manager = Manager()
    queue = manager.Queue(len(data))
    result_dict = manager.dict()

    for file in data:
        queue.put((file, path_to_dir))

    task1 = Process(target=count_words, args=(queue, result_dict))
    task2 = Process(target=count_words, args=(queue, result_dict))

    task1.start()
    task2.start()

    task1.join()
    task2.join()

    result_dict['total'] = sum(result_dict.values())
    return result_dict
