#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import os


def foo(filename, q):
    with open(filename, 'r') as file:
        words = file.read().rstrip(' ').split()
        q.put([filename.split('/')[-1], len(words)])


def word_count_inference(path_to_dir):
    procs = []
    q = Queue()
    res_dic = {}

    for f in os.listdir(path_to_dir):
        proc = Process(target=foo,
                       args=(os.path.join(path_to_dir, f), q))
        procs.append(proc)
        proc.start()

    _sum = 0
    for proc in procs:
        res = q.get()
        res_dic[res[0]] = res[1]
        _sum += res[1]

    res_dic["total"] = _sum
    return res_dic