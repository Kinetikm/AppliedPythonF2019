#!/usr/bin/env python
# coding: utf-8

from multiprocessing.dummy import Pool
from functools import partial
import os


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
    files = os.listdir(path_to_dir)
    our_dict, our_dict['total'] = {}, 0
    func = partial(dict_count, path_to_dir, our_dict)
    pool = Pool(os.cpu_count())
    pool.map(func, files)
    return our_dict


def file_read(path_to_dir, filename):
    """
    Читаем файл.
    :param path_to_dir:
    :param filename:
    :return: число слов
    """
    with open(path_to_dir + '/' + filename, "r") as file:
        return len(file.read().split())


def dict_count(path_to_dir, our_dict, filename):
    """
    Меняем наш словарь.
    :param path_to_dir:
    :param filename:
    :param our_dict:
    :return:
    """
    count = file_read(path_to_dir, filename)
    our_dict[filename] = count
    our_dict['total'] += count
