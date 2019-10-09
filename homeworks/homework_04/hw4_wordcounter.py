#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
from multiprocessing import Pool
import os


def words_in_file(queue, path):
    with open(path) as infile:
        words = 0
        for line in infile:
            words += len(line.split())
    queue.put((path, words))


def get_result(queue):
    result = {}
    while True:
        value = queue.get()
        if value:
            result[value[0].split('/')[-1]] = value[1]
        else:
            result['total'] = sum(result.values())
            return result


def word_count_inference(path_to_dir):
    q = Manager().Queue()
    processes = []
    files = os.listdir(path_to_dir)
    pool = Pool(5)
    result = pool.apply_async(get_result, args=(q,))
    for value in files:
        p = pool.apply_async(words_in_file, args=(q, path_to_dir + '/' + value,))
        processes.append(p)
    for p in processes:
        p.get()
    q.put(0)
    pool.close()
    pool.join()
    return result.get()
