#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import os
import threading
import time


class Task:
    def __init__(self, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        print("task {}".format(args))
        self.args = args
        self.kwargs = kwargs

    def perform(self, worker):
        for arg in self.args:
            print("perform", self.args, arg, os.getpid(), "worker: ", worker)
            time.sleep(arg*3)
        print("end:", os.getpid(), "args:", self.args, "worker: ", worker)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, my_number):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.queue = tasks_queue
        self.my_number = my_number
        print(my_number)
        self.tasks = []

    def run(self):
        task = self.queue.get()
        process = Process(target=task.perform, args=(self.my_number, ))
        self.tasks += [process]
        process.start()

    def join(self):
        for task in self.tasks:
            task.join()


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        sem = threading.BoundedSemaphore(self.n_workers)
        processors = []
        for i in range(self.n_workers):
            processor = TaskProcessor(queue, i)
            processors += [processor]
        while not self.queue.empty():
            for processor in processors:
                processor.run()
                if self.queue.empty():
                    break
        for processor in processors:
            processor.join()


manager = Manager()
queue = manager.Queue()
for i in range(10):
    queue.put(Task(i, 11-i))
tm = TaskManager(queue, 5, 10)
tm.run()
