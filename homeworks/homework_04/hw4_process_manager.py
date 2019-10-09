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
    def __init__(self, ...):
        """
        Пофантазируйте, как лучше инициализировать
        """
        raise NotImplementedError

    def perform(self):
        """
        Старт выполнения задачи
        """
        raise NotImplementedError


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, time_dict):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.ta_queue = tasks_queue
        self.t_dict = time_dict

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            task = ta_queue.get()

            task_s_time = time.time()
            pid = os.getpid()
            self.t_dict[pid] = task_s_time

            task.perform()




class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.t_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

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
        wid_s_time = manager.dict()
        workers = {}

        for _ in range(self.n_workers):
            worker = TaskProcessor(self.t_queue, wid_s_time)
            worker.start()
            workers[worker.pid] = worker

        while True:
            # restart
            for wid, w in workers.items():
                if not w.is_alive():
                    # если не пусто в множестве тасков!
                    new_w = TaskProcessor(self.t_queue, wid_s_time)
                    new_w.start()
                    workers[wid] = new_w
            # kill         
            wid_s_time_now = copy.deepcopy(wid_s_time)
            current_time = time.time()
            for wid, task_start_time in wid_s_time_now.items():
                if current_time - task_start_time > timeout:
                    timeouted_worker = workers[wid]
                    timeouted_worker.close()
                    timeouted_worker.join()

    # QUEUE
    # завершение мастер процесса, когда все таски выполнены!                

