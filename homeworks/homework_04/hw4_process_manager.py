#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from time import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        print("Start with task")
        self.func(*self.args, **self.kwargs)
        print("Finished with task")

class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.timeout = timeout
        self.process = None

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_queue.empty():
                break
            task = self.tasks_queue.get()
            self.process = Process(target=task.perform)
            self.process.start()
            self.process.join(timeout=self.timeout)
            self.process.terminate()

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
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.workers = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for i in range(len(self.n_workers)):
            proc = Process(target=TaskProcessor(self.tasks_queue, self.timeout).run)
            proc.start()
            self.workers.append(proc)

        while True not self.tasks_queue.empty():
            if self.tasks_queue.empty():
                break
            for i in range(len(self.workers)):
                if not self.workers[i].is_alive():
                    print("Start new process")
                    self.processes[i] = Process(target=TaskProcessor(self.tasks_queue, self.timeout).run)
                    self.processes[i].start()
