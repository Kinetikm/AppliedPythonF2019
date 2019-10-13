#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue
import time
import uuid


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

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self.func(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.task_queue = tasks_queue
        """
        random id for worker
        """
        self.id = uuid.uuid4()
        self.start = 0

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def __hash__(self) -> int:
        return self.id.__hash__()

    def run(self):
        """
        Старт работы воркера
        """
        self.start = time.time()
        while not self.task_queue.empty():
            task = self.task_queue.get()
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
        self.__queue = tasks_queue
        self.__n_workers = n_workers
        self.__timeout = timeout
        self.__workers = [TaskProcessor(self.__queue) for _ in range(self.__n_workers)]
        self.__active_process = {}

    def check_workers(self):
        while True:
            for_terminate_by_timeout = []
            for w, p in self.__active_process.items():
                if p.is_alive() and time.time() - w.start > self.__timeout:
                    for_terminate_by_timeout.append(w)
                    p.terminate()
                elif not p.is_alive():
                    del self.__active_process[w]
                    proc = Process(target=w.run())
                    self.__active_process[w] = proc
                    proc.start()

            for w in for_terminate_by_timeout:
                del self.__active_process[w]
                proc = Process(target=w.run())
                self.__active_process[w] = proc
                proc.start()
            time.sleep(.1)

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for worker in self.__workers:
            proc = Process(target=worker.run())
            self.__active_process[worker] = proc
            proc.start()
        check_process = Process(target=self.check_workers())
        check_process.start()


def qrt(k):
    time.sleep(k)
    print(k * k)


if __name__ == '__main__':
    q = Queue()

    for i in range(7):
        q.put(Task(qrt, i))
        print('put{}'.format(i))

    task_manager = TaskManager(q, 5, 10)
    task_manager.run()
