#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
from hw4_wordcounter import word_count_inference


class Task:
    def __init__(self, target, *args, **kwargs):
        self.target = target
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        self.target(*self.args, **self.kwargs)


class TaskProcessor:
    def __init__(self, tasks_queue):
        self.queue = tasks_queue
        self.task = None

    def run(self):
        task = self.queue.get()
        process = Process(target=task.perform)
        self.task = process
        process.start()

    def join(self, timeout):
        self.task.join(timeout)
        if self.task.is_alive():
            self.task.terminate()
        self.task = None

    def is_alive(self):
        if self.task is None:
            return False
        if self.task.is_alive():
            return True
        else:
            return False


class TaskManager:
    def __init__(self, tasks_queue, n_workers, timeout):
        self.queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        processors = []
        for i in range(self.n_workers):
            processor = TaskProcessor(queue)
            processors.append(processor)
        while not self.queue.empty():
            for processor in processors:
                processor.run()
                if self.queue.empty():
                    break
            for processor in processors:
                if processor.is_alive():
                    processor.join(self.timeout)


'''
manager = Manager()
queue = manager.Queue()
a = (1,2,3,4,5)
task = Task(print, 1)
queue.put(task)
queue.put(Task(print,a))
queue.put(Task(sum, a))
queue.put(Task(word_count_inference, "./homeworks/homework_04/test_data"))
tm = TaskManager(queue, 2, 10)
tm.run()
'''