#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Pool, Manager
import time
import os
import copy


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, args, kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.func = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.func(*self.args, **self.kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, time_dict):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.task_queue = tasks_queue
        self.t_dict = time_dict

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            task = task_queue.get()

            task_start_time = time.time()
            pid = os.getpid()
            self.t_dict[pid] = task_start_time

            task.perform()


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout, queue_timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        :param q_timeout: таймаут в секундах, из очереди пытаемся достать элемент q_timeout секунд
        """
        self.t_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.q_timeout = queue_timeout

    def run(self):
        """
        Запускайте бычка! (с)
        Мастер следит, что число воркеров всегда было равно n_workers (в случае смерти пересоздает их).
        """
        # создали пул рабочих, создали рабочих, передали в них очередь, запустили
        # pool = Pool(self.n_workers)
        # создать дикт из pid, TaskProccessor
        # создать queue для отслеживания времени выполнения, в который дочерний процесс будет записывать pid процесса, который
        # работает дольше положенного
        manager = Manager()
        # pid: task_start_time
        self.wid_task_start_time = manager.dict()
        # pid: TaskProcessor
        self.workers = {}

        for _ in range(self.n_workers):
            worker = TaskProcessor(self.t_queue, self.wid_task_start_time)
            worker.start()
            self.workers[worker.pid] = worker

        while True:
            # restart
            self.process_restart()
            # kill         
            self.kill_after_timeout

    def process_restart(self):
        new_workers_dict = {}
        for wid, w in self.workers.items():
            if not w.is_alive():
                new_worker = TaskProcessor(self.t_queue, self.wid_task_start_time)
                new_worker.start()
                new_workers_dict[new_worker.pid] = new_worker
            else:
                new_workers_dict[wid] = w

        self.workers = new_workers_dict

    def kill_after_timeout(self, timeout):
        current_time = time.time()
        # из-за многопроцессорности ФРИЗИМ состояние дикта!
        wid_task_start_time_curr = copy.deepcopy(self.wid_task_start_time)
        for wid, task_start_time in wid_task_start_time_curr.items():
            if current_time - task_start_time > timeout:
                timeouted_worker = self.workers[wid]
                # убили процесс
                timeouted_worker.terminate()
                # чтобы не было зомби процесса
                timeouted_worker.join()             
