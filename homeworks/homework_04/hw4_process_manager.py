#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self.function(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout):
        self.tasks = tasks_queue
        self.timeout = timeout
        self.time = 0
        self.run()

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            if not self.tasks.empty():
                task = self.tasks.get()
                process = Process(target=task.perform)
                process.start()
                self.time = time.time()
                while True:
                    if process.is_alive():
                        if time.time() - self.time >= self.timeout:
                            process.terminate()
                    else:
                        break
                process.join()


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
        self.tasks = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        processes = []
        for _ in range(self.n_workers):
            process = Process(target=TaskProcessor, args=(self.tasks, self.timeout))
            processes.append(process)
            process.start()
        for proc in processes:
            proc.join()
