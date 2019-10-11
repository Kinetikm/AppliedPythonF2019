#!/usr/bin/env python
# coding: utf-8

import multiprocessing as mp
from multiprocessing import Process


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, somefunc, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.args = args
        self.kwargs = kwargs
        self.somefunc = somefunc
        # raise NotImplementedError

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.somefunc(*self.args, **self.kwargs)
        print("something happend...")
        # raise NotImplementedError


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        # raise NotImplementedError

    def run(self, timeout):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_queue.empty():
                print("end has been reached")
                break
            task = self.tasks_queue.get()
            job = Process(target=task.perform())
            job.start()
            job.join(timeout)
            job.terminate()

        # raise NotImplementedError


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
        self.alive_processes = []
        # raise NotImplementedError

    def run(self):
        """
        Запускайте бычка! (с)
        """
        flag = self.tasks_queue.empty()
        tasks = [TaskProcessor(self.tasks_queue) for i in xrange(n_workers)]
        for task in tasks:
            job = Process(target=task.run(self.timeout))
            self.alive_processes.append(job)
            job.start()
        while flag is not True:
            index = 0
            for task in self.alive_processes:
                if not self.alive_processes[index].is_alive():
                    job = Process(target=tasks[index].run(self.timeout))
                    job.start()
            flag = self.tasks_queue.empty()
        # raise NotImplementedError
