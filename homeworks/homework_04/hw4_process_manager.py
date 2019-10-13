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

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        if not tasks_queue.empty():
            self.task = tasks_queue.get()
            if isinstance(self.task, Task):
                self.proc = Process(target=self.task.perform)
                self.start_time = 0
                self.timeout = timeout
                self.status_code = 0
            else:
                raise ValueError
        else:
            raise Exception("Queue End")

    def run(self):
        """
        Старт работы воркера
        """
        self.proc.start()
        self.start_time = time.time()
        delay = self.timeout/10
        time.sleep(delay)
        while time.time() - self.start_time < self.timeout:
            if self.proc.is_alive():
                time.sleep(delay)
            else:
                self.proc.terminate()
                self.status_code = 1
                break
        if self.status_code == 0:
            self.proc.terminate()
            self.status_code = -1


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
        """
        Запускайте бычка! (с)
        """
        workers = [None]*self.n_workers
        while not self.queue.empty():
            try:
                for i in range(self.n_workers):
                    if workers[i] is not None:
                        if workers[i].status_code != 0:
                            workers[i] = TaskProcessor(self.queue, self.timeout)
                            workers[i].run()
                    else:
                        workers[i] = TaskProcessor(self.queue, self.timeout)
                        workers[i].run()
            except Exception as e:
                if str(e) == "Queue End":
                    break
                else:
                    continue
        time.sleep(self.timeout)
