#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
from time import time, sleep
import os


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    # можно было бы сделать абстрактный класс (унаследовать от ABC)
    # и abstractmethod, но так не интересно)

    def __init__(self, code=None, is_path_to_file=False):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.code = code
        self.is_path_to_file = is_path_to_file

    def perform(self):
        """
        Старт выполнения задачи
        """
        if self.code:
            if self.is_path_to_file:
                with open(self.code, encoding='utf-8') as file:
                    exec(file.read())
            else:
                exec(self.code)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.proc = None
        self.q = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """
        task = self.q.get()
        self.proc = Process(target=task.perform, args=())
        self.proc.start()
        self.start_time = time()

    def is_alive(self):
        if self.proc:
            return self.proc.is_alive()
        return False

    def get_time(self):
        return self.start_time

    def terminate(self):
        self.proc.terminate()

    def get_pid(self):
        return self.proc.pid


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """

    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах,
        воркер не может работать дольше, чем timeout секунд
        """
        self.q = tasks_queue
        self.w_num = n_workers
        self.timeout = timeout
        self.workers = []
        self.time_start = []

    def run(self):
        SLEEP_TIME = 1
        while self.workers or not self.q.empty():
            if not self.q.empty():
                if self.w_num > self.q.qsize():
                    self.w_num = self.q.qsize()
                if self.timeout < SLEEP_TIME:
                    SLEEP_TIME = self.timeout
                while len(self.workers) < self.w_num:
                    self.workers.append(TaskProcessor(self.q))
                    self.workers[-1].run()
                    print(f"Start new process {self.workers[-1].get_pid()}")
                    self.time_start.append(self.workers[-1].get_time())
            i = 0
            while i < len(self.workers):
                if not self.workers[i].is_alive():
                    print(f"Process {self.workers[i].get_pid()} died")
                    del self.workers[i]
                    del self.time_start[i]
                i += 1
            for i in range(len(self.workers)):
                is_alive = self.workers[i].is_alive()
                if is_alive and time() - self.time_start[i] > self.timeout:
                    p = self.workers[i].get_pid()
                    print(f"Time limit exceeded. Terminate process {p}")
                    self.workers[i].terminate()
            sleep(SLEEP_TIME)


'''if __name__ == '__main__':
    manager = Manager()
    queue = manager.Queue()
    # Можно ручками вводить
    n = int(input("Введите количество тасков"))
    n = 5
    py_code = 'print("Hello world!!!")'
    for _ in range(n)
        queue.put(Task(py_code))
    # можно с одного файла читать по команде
    path_to_file = 'py_code.py'
    with open(path_to_file, 'r', encoding='utf-8') as file:
        for line in file:
            queue.put(Task(line))
    # самое интересное, как мне кажется
    path_to_dir = 'test_for_hw4'
    files = os.listdir(path_to_dir)
    for file in files:
        queue.put(Task(path_to_dir + '/' + file, True))
    TIMEOUT = 20
    WORKER_NUMBER = 5
    task_manager = TaskManager(queue, WORKER_NUMBER, TIMEOUT)
    task_manager.run()'''
