#!/usr/bin/env python
# coding: utf-8

import time
import signal
import os
import multiprocessing
from multiprocessing import Process


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    # это нельзя сериализовать(
    # State = Enum('TaskState', 'new done error locked')
    # '''
    #     :param new: new task
    #     :param done: task performed correctly
    #     :param error: there was some exception during performing task
    # '''

    def __init__(self):  # , qid, version=0, args=..., kwargs=...):
        """
        Пофантазируйте, как лучше инициализировать

        :param qid: id виртуальной очереди, которая должна быть зарегистрирована в TaskManager
        """

        # Можно было сделать как Process. Но тогда бы не получилось сохранить данные о задаче во внешнем хранилище,
        # потому что мы не можем сериализовать функции
        # а идея разгребальщика очередей как раз в том, чтобы нагрузку можно было распределить и
        # передать данные, необходимые для обработки этой задачи на другую тачку.
        # Но если мы храним очереди во внешнем хранилище, то возникают проблемы с тем, чтобы
        # код разгребальщиков и код, который добалвяет очерди был одинаковый. Для того, чтобы не плодить очереди
        # когда меняется логика, можно сделать версионирование, но логику работы с разными версиямы нужно будет
        # реализовать в perform
        # хотя, для задания это все вообще не нужно..
        # self.qid = qid
        # self.version = version
        # self.args = args
        # self.kwargs = kwargs
        self.state = "new"

    def perform(self):
        """
        Старт выполнения задачи.
        Должен быть пепреопределен в дочернем классе таски.
        """
        raise NotImplementedError


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    need_stop = False

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.start_time = time.time()
        self.process = None

    def is_too_old(self, timeout):
        return time.time() >= timeout + self.start_time

    def run(self):
        """
        Старт работы воркера
        """

        def sigusr1_handler(signum, frame):
            TaskProcessor.need_stop = True

        signal.signal(signal.SIGHUP, sigusr1_handler)

        while True:
            task = self.tasks_queue.get()
            try:
                task.state = "locked"
                task.perform()
                task.state = "done"
            except Exception as e:
                print("cant process task:", task, "because", e)
                task.state = 'error'

            if self.need_stop:
                break


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout, check_worker_alive_timeout=1,
                 worker_graceful_shutdown_timeout=10):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.task_queue = tasks_queue
        self.n_workers = n_workers
        self.worker_timeout = timeout

        self.workers = dict()  # pid -> Process

        self.check_worker_alive_timeout = check_worker_alive_timeout
        self.worker_graceful_shutdown_timeout = worker_graceful_shutdown_timeout

    def start_worker(self):
        tp = TaskProcessor(self.task_queue)
        try:
            worker = Process(target=lambda tp: tp.run(), args=(tp,))
            worker.start()

            tp.process = worker
            print("starting worker", worker.pid)
            self.workers[worker.pid] = tp

        except multiprocessing.ProcessError as e:
            print("cant run new worker:", e)

    def stop_worker(self, pid):
        if pid not in self.workers:
            return
        worker = self.workers[pid]
        os.kill(pid, signal.SIGHUP)

        wait_for_worker = self.worker_graceful_shutdown_timeout
        worker.process.join(wait_for_worker)
        worker.process.terminate()

        time.sleep(0.1)
        if worker.process.is_alive():
            os.kill(worker.process.pid, signal.SIGKILL)

        del self.workers[pid]

        return

    def stop_workers(self):
        for pid in self.workers.copy():
            print("stopping worker", pid)
            self.stop_worker(pid)

        return

    def run(self, once=False):
        """
        Запускайте бычка! (с)
        :param once: елси True, то когда истечет таймаут воркеров, исполенние прекратится
        """

        for i in range(self.n_workers):
            self.start_worker()

        while True:
            for pid in self.workers.copy():
                if pid not in self.workers:
                    continue

                worker = self.workers[pid]
                if not worker.process.is_alive():
                    del self.workers[pid]
                if worker.is_too_old(self.worker_timeout):

                    self.stop_worker(worker.process.pid)

            for i in range(self.n_workers - len(self.workers)):
                if once and len(self.workers) == 0:
                    return
                if once:
                    break
                self.start_worker()

            time.sleep(self.check_worker_alive_timeout)

        self.stop_workers()

        return
