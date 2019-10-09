#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Queue, Pool
import os


def word_count_inference(path_to_dir):
    manager = Manager()
    q = manager.Queue()
    words = manager.dict()
    files = [path_to_dir + "/" + i for i in os.listdir(path_to_dir)]
    pool = Pool(5)
    result = pool.apply_async(f_c, args=(q, words))

    for i in files:
        p = pool.apply_async(f, args=(i, q, words))
        p.get()

    queue.put(-5)
    return result.get()


def f(file, q, words):
    with open(file, 'r') as file:
        tmp = 0
        for line in file:
            tmp += len(line.split())

        words[file.split('/')[-1]] = tmp
        q.put(tmp)


def f_c(q, words):
    res = 0
    while True:
        tmp = q.get()
        if tmp == -5:
            break
        res += tmp

    words['total'] = res
    return dict(words)
