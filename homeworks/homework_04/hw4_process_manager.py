#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Process
from time import sleep


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, foo, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.foo = foo
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.foo(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """
        task = self.tasks_queue.get()
        task.perfom()


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
        self.prs = list()

    def start_process(self):
        work = TaskProcessor(self.tasks_queue)
        process = Process(target=work.run)
        self.prs.append(process)
        process.start()

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while not self.tasks_queue.empty():
            if self.tasks_queue.qsize() < self.n_workers:
                self.n_workers = self.tasks_queue.qsize()
            for i in range(self.n_workers):
                self.start_process()
        sleep(self.timeout)
        for item in self.prs:
            item.terminate() if item.is_alive() else item.join()
