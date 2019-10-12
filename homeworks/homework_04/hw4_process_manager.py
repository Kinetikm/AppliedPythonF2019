#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import time
from random import randint

class Task:
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        print("start")
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    def __init__(self, tasks_queue):
        self.tasks_queue = tasks_queue


    def run(self, timeout):
        while not (self.tasks_queue.empty()):
            task = self.tasks_queue.get()
            process = Process(target=task.perform)
            process.start()
            process.join(timeout)
            process.terminate()



class TaskManager:
    def __init__(self, tasks_queue, n_workers, timeout):
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.workers = []


    def run(self):
        task_tmp = [TaskProcessor(self.tasks_queue) for _ in range(self.n_workers)]
        for task in task_tmp:
            process = Process(target=task.run(self.timeout))
            self.workers.append(process)
            process.start()
        while not self.tasks_queue.empty():
            for task in self.workers:
                if not self.workers[i].is_alive():
                    process = Process(target=self.workers[i].run(self.timeout))
                    process.start
