#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Queue, current_process
import time
import random


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, args=(), kwargs={}):
        """
        :param func: функция, которую надо выполнить
        :param args: позиционные аргументы функции в виде списка
        :param kwargs: именнованные аргументы функции в виде словаря
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.name = func.__name__

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self.func(*self.args, **self.kwargs)

    def __str__(self):
        return f'Task obj: func = {self.name}, args = {self.args}, kwargs = {self.kwargs}'


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param done_queue: Manager.Queue со строками - результами выполнения таски
        """
        self.tasks_queue = tasks_queue
        self.start_time = time.time()
        self.p = None
        self.name = None

    def calculate(self):
        for task in iter(self.tasks_queue.get, 'STOP'):
            result = task.perform()
            args_str = ', '.join(str(i) for i in task.args)
            kwargs_str = ', '.join('='.join((str(k), str(v))) for k, v in task.kwargs.items())
            # попытка красиво вывести результат выполнения воркера
            job_info = f'{current_process().name} says that {task.name}({args_str} {kwargs_str}) = {result}'
            print(job_info)

    def run(self):
        """
        Старт работы воркера
        """
        self.p = Process(target=self.calculate)
        self.name = self.p.name
        self.p.start()

    def suicide(self):
        self.p.terminate()

    def finish(self):
        self.p.join()

    def is_alive(self):
        return self.p.is_alive()


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
        self.workers = []

    def start_worker(self):
        p = TaskProcessor(self.tasks_queue)
        self.workers.append(p)
        p.run()

    def run(self):
        """
        Запускайте бычка! (с)
        """
        for _ in range(self.n_workers):
            self.start_worker()

        # Проверяем, не работает ли какой-нибудь воркер дольше таймаута
        while not self.tasks_queue.empty():
            for worker in self.workers:
                if worker.is_alive():
                    if time.time() - worker.start_time >= self.timeout:
                        print(f'{worker.name} timeout! termiate')
                        worker.suicide()
                        worker.finish()
                        self.workers.remove(worker)

                        self.start_worker()
            time.sleep(0.1)

    def stop(self):
        for _ in range(self.n_workers):
            self.tasks_queue.put('STOP')

        for w in self.workers:
            w.finish()


if __name__ == "__main__":
    def mul(a, b):
        # Эта функция может работать за время большее, чем таймаут
        time.sleep(2*random.random())
        return a * b

    def plus(a, b):
        time.sleep(0.5*random.random())
        return a + b

    def say_hello(name):
        time.sleep(0.5*random.random())
        return 'Hello ' + name

    tasks_queue = Queue()

    # Заполним очередь первой таской
    for i in [Task(mul, (j, 7)) for j in range(20)]:
        tasks_queue.put(i)

    # создадим и запустим менеджера
    NUMBER_OF_PROCESSES = 4
    TIMEOUT = 1
    tm = TaskManager(tasks_queue, NUMBER_OF_PROCESSES, TIMEOUT)
    tm.run()

    # Добавим в очередь вторую таску
    for i in [Task(plus, (j, 7)) for j in range(20)]:
        tasks_queue.put(i)
    # Добавим в очередь третью таску
    for i in [Task(say_hello, kwargs={'name': j}) for j in ('Vasya', 'Petya', 'Kolya')]:
        tasks_queue.put(i)

    tm.stop()
