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
        if not self.kwargs:
            if not self.args:
                r = self.func()
            else:
                r = self.func(*self.args)
        else:
            if not self.args:
                r = self.func(**self.kwargs)
            else:
                r = self.func(*self.args, **self.kwargs)
        return r


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super().__init__()
        self.queue = tasks_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """
        while True:
            procc = self.queue.get()
            proces = Process(target=procc.perform, args=())
            proces.start()
            time.sleep(self.timeout)
            if proces.is_alive():
                proces.terminate()
                print('terminated ' + str(procc))
            else:
                proces.join()


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
        self.__workers = []
        self.__num_workers = n_workers
        self.__timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        while True:
            try:
                self.__workers.extend([TaskProcessor(self.__queue, self.__timeout).start()
                                       for _ in range(self.__num_workers - len(self.__workers))])
            except Exception:
                continue


def func_sleep(a, b):
    time.sleep(a)
    print(b)


queue = Manager().Queue()
for i in range(5):
    queue.put(Task(func_sleep, i, i*i))
    print(f'put {i}')


tm = TaskManager(queue, 5, 12)
proc = Process(target=tm.run, args=())
proc.start()


for i in range(5, 10):
    queue.put(Task(func_sleep, a=i, b=i*i))
    print(f'put {i}')

for i in range(10, 15):
    queue.put(Task(func_sleep, i, b=i*i))
    print(f'put {i}')


proc.join()
