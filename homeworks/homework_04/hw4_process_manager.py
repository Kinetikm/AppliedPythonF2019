#!/usr/bin/env python
# coding: utf-8

import multiprocessing as mp


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
        self.func(self.args, self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        if not tasks_queue.empty():
            val = tasks_queue.get()
            self.task = val
            self.process = mp.Process(target=val.perform())

    def run(self):
        """
        Старт работы воркера
        """
        self.process.start()


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
        self.job = dict(enumerate(self.n_workers))

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while not self.tasks_queue.empty():
            for worker, val in self.job:
                val.append(TaskProcessor(self.tasks_queue))
                val.run()
            for worker, val in self.job:
                val.join(timeout=self.timeout)
                if not val.is_alive():
                    if not self.tasks_queue.empty():
                        self.job[worker] = TaskProcessor(self.tasks_queue)
                        self.job[worker].run()
