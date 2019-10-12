import os
import signal
from time import sleep, time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, function, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self.function(*self.args, **self.kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.task = tasks_queue.get()

    def run(self):
        """
        Старт работы воркера
        """
        self.task.perform()


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
        self.tasks = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
'''
        processes = []

        while not self.tasks.empty():
            if self.n_workers < self.tasks.qsize():
                for _ in range(self.n_workers):
                    worker = TaskProcessor(self.tasks)
                    proc = Process(target=worker.run)
                    processes.append(proc)
                    proc.start()
            else:
                for _ in range(self.tasks.qsize()):
                    worker = TaskProcessor(self.tasks)
                    proc = Process(target=worker.run)
                    processes.append(proc)
                    proc.start()

        sleep(self.timeout)
        for proc in processes:
            if proc.is_alive():
                proc.terminate()
                print('proc is terminated')
            else:
                proc.join()
'''

        pool = Pool(5)
        