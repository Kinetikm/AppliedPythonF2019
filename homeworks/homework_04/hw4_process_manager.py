#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, target, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self._target(*self._args, **self._kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._tasks_queue = tasks_queue
        self._timeout = timeout
        self._proc = None

    def run(self):
        """
        Старт работы воркера
        """
        while not self._tasks_queue.empty():
            task = self._tasks_queue.get()
            self._proc = Process(target=task.perform)
            self._proc.start()
            self._proc.join(timeout=self._timeout)
            self._proc.terminate()


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
        self._tasks_queue = tasks_queue
        self._n_workers = n_workers
        self._timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        workers = []
        for i in range(self._n_workers):
            workers.append(TaskProcessor(self._tasks_queue, self._timeout, i))

        proc_list = []

        for worker in workers:
            proc = Process(target=worker.run)
            proc_list.append(proc)
            proc.start()

        while not self._tasks_queue.empty():
            for i in range(self._n_workers):
                if not proc_list[i].is_alive():
                    proc_list[i].terminate()
                    workers[i] = TaskProcessor(self._tasks_queue, self._timeout, i)
                    proc = Process(target=workers[i].run)
                    proc_list[i] = proc
                    proc.start()
