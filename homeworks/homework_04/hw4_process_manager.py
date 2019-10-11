#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from threading import Thread

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
        return self.func(*self.args, **self.kwargs)

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

    def run(self):
        """
        Старт работы воркера
        """
        while not self.tasks_queue.empty():
            new_task = self.tasks_queue.get()
            t = Process(target=new_task.perform, args=())
            t.start()
            t.join(timeout=self.timeout)
            t.terminate()

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
        self.n = n_workers
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        processes = []
        for i in range(self.n):
            p = Process(target=self.run_worker, args=())
            processes.append(p)
            p.start()
        for i in processes:
            i.join()

    def run_worker(self):
        while not self.tasks_queue.empty():
            newTP = TaskProcessor(self.tasks_queue, self.timeout)
            newTP.run()