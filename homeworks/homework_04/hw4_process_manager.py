#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue, Manager
from abc import ABC, abstractmethod
from time import time, sleep

class Task(ABC):

    @abstractmethod
    def perform(self):
        pass

class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.start_t = 0
        self.process = None
        self.pid = None

    def run(self):
        """
        Старт работы воркера
        """
        Task = self.tasks_queue.get()
        self.process = Process(target=Task.perform, args=())
        self.process.start()
        self.start_t = time()
        self.pid = self.process.pid

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

    def add_process(self, w_list):
        worker = TaskProcessor(self.tasks_queue)
        w_list.append(worker)
        worker.run()
        print(f'Процесс {worker.pid} запущен.')

    def run(self):
        work_list = []
        sleeptime = 1
        for _ in range(self.n_workers):
           self.add_process(work_list)
        while not self.tasks_queue.empty():
            k = 0
            for i in range(len(work_list)):
                pid = work_list[i - k].pid
                if work_list[i - k].process.is_alive():
                    if time() - work_list[i - k].start_t > self.timeout:
                        print(f'Процесс {pid} удален по превышению времени.')
                        del work_list[i - k]
                        k += 1
                        if not self.tasks_queue.empty():
                            self.add_process(work_list)
                else:
                    print(f'Процесс {pid} удален по выполнению задачи.')
                    del work_list[i - k]
                    k += 1
                    if not self.tasks_queue.empty():
                        self.add_process(work_list)
            sleep(sleeptime)
        while len(work_list) != 0:
            k = 0
            for i in range(len(work_list)):
                pid = work_list[i - k].pid
                if work_list[i - k].process.is_alive():
                    if time() - work_list[i - k].start_t > self.timeout:
                        print(f'Процесс {pid} удален по превышению времени.')
                        del work_list[i - k]
                        k += 1
                else:
                    print(f'Процесс {pid} удален по выполнению задачи.')
                    del work_list[i - k]
                    k += 1
            sleep(sleeptime)
        print("Дело сделано.")
