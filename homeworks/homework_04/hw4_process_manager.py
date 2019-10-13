#!/usr/bin/env python
# coding: utf-8

from queue import Empty
from multiprocessing import Process, Manager, Queue
from time import time, sleep


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, target, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self._target = target
        self._args = args
        self._kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self._target(*self._args, **self._kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._tasks_queue = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            try:
                task = self._tasks_queue.get(block=True)  # ждем пока что нибудь появится в очереди
            except EOFError:  # ловим terminate на процесс-родитель (task manager)
                return
            task.perform()


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
        self._queue = tasks_queue
        self._workers_num = n_workers
        self._timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        active_workers_p = []
        while True:
            available = self._workers_num - len(active_workers_p)
            for worker in range(available):
                processor = TaskProcessor(self._queue)
                active_worker = Process(target=processor.run)
                active_worker.start()
                active_workers_p.append((active_worker, time()))
            new_active_workers_p = []
            for active_worker, start_time in active_workers_p:
                if active_worker.is_alive():
                    if time() - start_time < self._timeout:
                        new_active_workers_p.append((active_worker, start_time))
                    else:
                        active_worker.terminate()
            active_workers_p = new_active_workers_p
            sleep(0.1)


if __name__ == "__main__":
    """Простые тесты"""

    def sleeper(i, stime):
        print(f"Start: {i}")
        sleep(stime)
        print(f"Finish: {i}")
        return i, stime

    manager = Manager()
    queue = manager.Queue()
    task_manager = TaskManager(queue, 4, 2)
    process = Process(target=task_manager.run)
    process.start()
    n = 2
    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=4))  # kwargs
        queue.put(Task(sleeper, it + n, 4))      # args
    sleep(2)
    assert queue.empty()

    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=1))  # kwargs
        queue.put(Task(sleeper, it + n, 1))      # args
    sleep(1)
    assert queue.empty()

    # не отваливаемся по timeout но часть воркеров не успеваю дообработать таски
    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=1))  # kwargs
        queue.put(Task(sleeper, it + n, 2))      # args
    sleep(2)
    assert queue.empty()
    process.terminate()
