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
        self._target(*self._args, **self._kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._task = tasks_queue.get()

    def run(self):
        """
        Старт работы воркера
        """
        process = Process(target=self._task.perform)
        process.start()
        return process


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
        active_processes = []
        while self._queue.empty() is False or len(active_processes) != 0:

            last = self._queue.qsize()
            available = self._workers_num - len(active_processes)
            for worker in range(min(last, available)):
                process = TaskProcessor(self._queue)
                active_processes.append((process.run(), time.time()))

            new_active_processes = []
            for process, start_time in active_processes:
                if process.is_alive():
                    if (time.time() - start_time) > self._timeout:
                        process.terminate()
                    else:
                        new_active_processes.append((process, start_time))
            active_processes = new_active_processes
            time.sleep(0.1)


if __name__ == "__main__":
    """Простые тесты"""

    def sleeper(i, stime):
        print(f"Start: {i}")
        time.sleep(stime)
        print(f"End: {i}")

    manager = Manager()
    queue = manager.Queue()
    for it in range(3):
        queue.put(Task(sleeper, i=it, stime=1))
        queue.put(Task(sleeper, it+3, 1))

    task_manager = TaskManager(queue, 4, 2)
    task_manager.run()
