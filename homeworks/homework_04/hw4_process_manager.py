#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.args = args
        self.kwargs = kwargs
        self.function = function

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue

    def run(self, timeout):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_queue.empty():
                print("end")
                break
            task = self.tasks_queue.get()
            work = Process(target=task.perform())
            work.start()
            work.join(timeout=timeout)
            work.terminate()


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
        self.alive_procs = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        tasks = []
        for i in range(n_workers):
            tasks.append(TaskProcessor(self.tasks_queue))
        for task in tasks:
            work = Process(target=task.run(timeout=self.timeout))
            self.alive_procs.append(work)
            work.start()
        while not self.tasks_queue.empty():
            for i in range(len(self.alive_procs)):
                if not self.alive_procs[i].is_alive():
                    work = Process(target=self.alive_procs[i].run(self.timeout))
                    work.start()
