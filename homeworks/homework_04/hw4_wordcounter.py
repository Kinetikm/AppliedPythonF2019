#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import os


def counter(path_to_dir, file, queue):
    quantity_words = 0
    path_to_file = path_to_dir + '/' + file

    with open(path_to_file, "r") as file_handler:
        for line in file_handler:
            quantity_words += len(line.split())

        message = file + ' ' + str(quantity_words)
        queue.put(message)


def combiner(queue, dictionary):
    while True:
        if queue.empty():
            continue

        result = queue.get()
        packet = result.split()

        print(result)
        print(packet)

        if result == "kill":
            break

        if result != '':
            dictionary[packet[0]] = int(packet[1])
            dictionary["total"] += int(packet[1])
        else:
            raise KeyError


def word_count_inference(path_to_dir):
    manager = Manager()
    queue = manager.Queue()
    result = manager.dict({"total": 0})

    collector = Process(target=combiner, args=(queue, result))
    collector.start()

    workers = []
    for file in os.listdir(path_to_dir):
        worker = Process(target=counter, args=(path_to_dir, file, queue))
        workers.append(worker)
        worker.start()

    for work in workers:
        work.join()

    queue.put("kill")
    collector.join()
    
    return result
