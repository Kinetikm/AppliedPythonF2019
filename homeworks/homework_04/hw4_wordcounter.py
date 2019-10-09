#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
from multiprocessing import Pool, Manager
import os


def word_count_inference(path_to_dir):
    files = [path_to_dir + "/" + i for i in os.listdir(path_to_dir)]
    manager = Manager()
    q = manager.Queue()
    words = manager.dict()
    pool = Pool(5)

    result = pool.apply_async(f_c, (q, words))

    for i in files:
        p = pool.apply_async(f, (i, q, words))
        p.get()

    q.put(-1)
    return result.get()


def f(file, q, words):
    with open(file, 'r') as f:
        tmp = 0
        for line in f:
            tmp += len(line.split())

        words[file.split('/')[-1]] = tmp
        q.put(tmp)


def f_c(q, words):
    total = 0
    while True:
        tmp = q.get()
        if tmp == -1:
            break
        total += tmp

    words['total'] = total
    return dict(words)
