#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
from time import sleep
from random import randint


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
        print(f'Start func: {self.func.__name__} with arguments {self.args, self.kwargs}')
        self.func(*self.args, **self.kwargs)
        print(f'Done func: {self.func.__name__} with result {self.func(*self.args, **self.kwargs)}')


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_q = tasks_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            if self.tasks_q.empty():
                break
            task = self.tasks_q.get()
            proc = Process(target=task.perform)
            proc.start()
            proc.join(self.timeout)
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
        """
        self.tasks_q = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.active_processes = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        workers = [TaskProcessor(self.tasks_q, self.timeout) for _ in range(self.n_workers)]
        for worker in workers:
            process = Process(target=worker.run)
            self.active_processes.append(process)
            process.start()
        while not self.tasks_q.empty():
            self.active_processes[randint(0, len(self.active_processes) - 1)].terminate()  # Для проверки
            for i, process in enumerate(self.active_processes):
                if not process.is_alive():
                    print('Create new process')
                    process = Process(target=workers[i].run)
                    process.start()
            sleep(2)


def sqr(n):
    sleep(n)
    return n ** 2


if __name__ == '__main__':
    q = Queue()
    n_workers_ = 4
    timeout_ = 7
    tasks = 20

    for j in range(tasks):
        q.put(Task(sqr, j))

    manager = TaskManager(q, n_workers_, timeout_)
    manager.run()
