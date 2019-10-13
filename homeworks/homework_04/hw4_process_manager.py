#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import time


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

    def __init__(self, tasks_queue, timeout_task):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.timeout_task = timeout_task

    def run(self):
        """
        Старт работы воркера
        """
        while not self.tasks_queue.empty():
            trg = self.tasks_queue.get()
            proc = Process(target=trg.perform)
            proc.start()
            try:
                proc.join(timeout=self.timeout_task)
            except:
                proc.terminate()


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """

    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд

        "Если какая-то задача выполняется дольше таймаута, то её выполнение должно прекратиться."
        потому добавим еще один параметр - timeout_task
        А значит, процессы в процессах, ибо время важно для воркера и для таски
        """
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.workers = [
            Process(target=TaskProcessor(tasks_queue=self.tasks_queue,
                                         timeout_task=self.timeout).run) for _
            in range(self.n_workers)]

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for worker in self.workers:
            worker.start()
        while True:
            for i, worker in enumerate(self.workers):
                if not worker.is_alive():
                    self.workers.pop(i)
                    tmp_proc = Process(
                        target=TaskProcessor(tasks_queue=self.tasks_queue,
                                             timeout_task=self.timeout).run)
                    tmp_proc.run()
                    self.workers.append(tmp_proc)
