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
        """
        Пофантазируйте, как лучше инициализировать
        """
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
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue
        self.proc = None
        self.time = None

    def run(self):
        """
        Старт работы воркера
        """
        if not self.tasks_queue.empty():
            task = self.tasks_queue.get()
            if not isinstance(task, Task):
                raise TypeError
            else:
                self.proc = Process(target=task.perform)
                self.proc.start()
                print('process {} start'.format(self.proc.pid))
                self.time = time.time()


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
        self.time_check = self.timeout / (self.n_workers + 1)

    def run(self):
        """
        Запускайте бычка! (с)
        """
        if self.n_workers < self.tasks_queue.qsize():
            for _ in range(self.n_workers):
                proceses = [TaskProcessor(tasks_queue=self.tasks_queue)]
        else:
            for _ in range(self.tasks_queue.qsize()):
                proceses = [TaskProcessor(tasks_queue=self.tasks_queue)]
        for proc in proceses:
            proc.run()
        while not self.tasks_queue.empty():
            for i in range(len(proceses)):
                if proceses[i].proc is None:
                    del proceses[i]
                    continue
                if not proceses[i].proc.is_alive():
                    print('proceses {} done'.format(proceses[i].proc.pid))
                    del proceses[i]
                    proceses.append(TaskProcessor(tasks_queue=self.tasks_queue))
                    proceses[-1].run()
                elif self.timeout:
                    if time.time() - proceses[i].time > self.timeout:
                        proceses[i].proc.terminate()
                        print('process {} was terminated'.format(proceses[i].proc.pid))
                        del proceses[i]
                        proceses.append(TaskProcessor(tasks_queue=self.tasks_queue))
                        proceses[-1].run()
            time.sleep(self.time_check)
        while len(proceses) != 0:
            k = 0
            while k < len(proceses):
                if proceses[i].proc is None:
                    del proceses[i]
                    continue
                if not proceses[i].proc.is_alive():
                    print('proceses {} done'.format(proceses[i].proc.pid))
                    del proceses[i]
                elif self.timeout:
                    if time.time() - proceses[i].time > self.timeout:
                        proceses[i].proc.terminate()
                        print('process {} was terminated'.format(proceses[i].proc.pid))
                        del proceses[i]
                k += 1
            time.sleep(self.time_check)


'''
manager = Manager()
queue = manager.Queue()
queue.put(Task())
a = TaskManager(queue, 1, 2)
a.run()
'''
