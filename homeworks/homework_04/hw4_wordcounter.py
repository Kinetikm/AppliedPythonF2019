#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os
import math


def word_count_inference(path_to_dir):

    files = os.listdir(path_to_dir)
    manager = Manager()
    dct = manager.dict()
    dct['total'] = 0
    procs = []
    for fl in files:
        proc = Process(target=count, args=((path_to_dir, fl), dct))
        proc.start()
        procs.append(proc)

    for pr in procs:
        pr.join()
    return dct


def count(path_to_file, dct):
    path = path_to_file[0] + '/' + path_to_file[1]
    path_to_file = path_to_file[1]
    dct[path_to_file] = 0
    with open(path, 'r', encoding="utf-8") as file:
        for ln in file:
            dct[path_to_file] += len(ln.split())
        dct['total'] += dct[path_to_file]
