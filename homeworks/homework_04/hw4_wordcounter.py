#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os
import math


def word_count_inference(path_to_dir):

    files = os.listdir(path_to_dir)
    manager = Manager()
    dct = manager.dict()
    queue = manager.Queue()
    for fl in files:
        queue.put((path_to_dir, fl))
    dct['total'] = 0
    PROCESSES_COUNT = 3
    pool = Pool(PROCESSES_COUNT)
    for i in range(queue.qsize()):
        pool.apply_async(count, (queue, dct))
    pool.close()
    pool.join()
    for key in dct:
        if key != 'total':
            dct['total'] += dct[key]
    return dct


def count(q, dct):
    pth = q.get()
    path = pth[0] + '/' + pth[1]
    dct[pth[1]] = 0
    with open(path, 'r', encoding="utf-8") as file:
        for ln in file:
            dct[pth[1]] += len(ln.split())
