#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager
import time
import os


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
        self.func_res = None

    def perform(self):
        """
        Старт выполнения задачи
        """
        res = self.func(*self.args, **self.kwargs)
        return res


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, num):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.num = num

    def run(self, start_new_task_time, result_queue):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_queue.full():
                task = self.tasks_queue.get()
                print(task)
                try:
                    start_new_task_time[self.num] = time.time()
                    res = task.perform()
                    result_queue.put((task, res))
                except Exception:
                    result_queue.put((task, 'Exception happens :('))
            else:
                break


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать
        дольше, чем timeout секунд
        """
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        result_queue = Manager().Queue()
        worker_and_his_process = {}
        start_work = Process(target=self.start_work, args=(
                             worker_and_his_process, result_queue))
        start_work.start()
        start_work.join()
        answ = []
        while result_queue.full:
            answ.append(result_queue.get())
        return answ

    def start_work(self, worker_and_his_process, result_queue):
        start_new_task_time = Manager().dict()
        for i in range(self.n_workers):
            worker = TaskProcessor(self.tasks_queue, i)
            worker_and_his_process[i] = [worker]
            new_proc = Process(target=worker.run, args=(
                                    start_new_task_time, result_queue))
            worker_and_his_process[i].append(new_proc)
            new_proc.start()
        while True:
            for i, val in start_new_task_time.items():
                if time.time() - val > self.timeout:
                    worker_and_his_process[i][1].kill()
                    worker_and_his_process[i][1].join()
                    result_queue.put('Timeout happens')
                    worker_and_his_process[i][1] = Process(
                               target=worker_and_his_process[i][0].run,
                               args=(start_new_task_time, result_queue))
                    worker_and_his_process[i][1].start()
            if all([not val[1].is_alive() for val in
                    worker_and_his_process.values()]):
                break
        for val in worker_and_his_process.values():
            val[1].join()
