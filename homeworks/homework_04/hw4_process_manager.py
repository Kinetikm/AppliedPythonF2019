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

    def run(self, result_queue):
        """
        Старт работы воркера
        """
        while not self._tasks_queue.empty():
            try:
                task = self._tasks_queue.get(block=False)
            except Empty:
                break
            result = task.perform()
            result_queue.put((task, result))


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
        result_queue = Queue(self._queue.qsize())
        while not self._queue.empty() or len(active_workers_p) != 0:
            last = self._queue.qsize()
            available = self._workers_num - len(active_workers_p)
            for worker in range(min(last, available)):
                processor = TaskProcessor(self._queue)
                active_worker = Process(target=processor.run, args=(result_queue, ))
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
        work_result = {}
        while not result_queue.empty():
            key, value = result_queue.get_nowait()
            work_result[key] = value
        return work_result


if __name__ == "__main__":
    """Простые тесты"""

    def sleeper(i, stime):
        print(f"Start: {i}")
        sleep(stime)
        print(f"Finish: {i}")
        return i, stime

    # отваливаемся по timeout
    manager = Manager()
    queue = manager.Queue()
    n = 3
    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=2))  # kwargs
        queue.put(Task(sleeper, it + n, 2))      # args

    task_manager = TaskManager(queue, 4, 1)
    res = task_manager.run()
    assert len(res) == 0
    print(res)

    # не отваливаемся по timeout
    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=2))  # kwargs
        queue.put(Task(sleeper, it + n, 2))      # args

    task_manager = TaskManager(queue, 4, 4)
    res = task_manager.run()
    assert len(res) == n * 2
    print(res)

    # не отваливаемся по timeout но часть воркеров не успеваю дообработать таски
    for it in range(n):
        queue.put(Task(sleeper, i=it, stime=2))  # kwargs
        queue.put(Task(sleeper, it + n, 2))  # args

    task_manager = TaskManager(queue, 4, 3)
    res = task_manager.run()
    print(res)
    assert len(res) == 4
