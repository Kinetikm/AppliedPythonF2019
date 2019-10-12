#!/usr/bin/env python
# coding: utf-8


from multiprocessing import Process
from signal import signal, SIGALRM, alarm
from inspect import iscoroutinefunction
import asyncio


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        try:
            self.func = kwargs.pop("func")
        except KeyError as K:
            raise KeyError(f"Where is a argument {K}, man?")

        self.args = args
        self.kwargs = kwargs
        self.is_async_func = True if iscoroutinefunction(self.func) else False
        # raise NotImplementedError

    def perform(self):
        """
        Старт выполнения задачи
        """
        if self.is_async_func:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.func(*self.args, **self.kwargs))
        else:
            self.func(*self.args, **self.kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    class TaskTimeoutError(TimeoutError):
        pass

    def timeout_handler(*args):
        raise TaskProcessor.TaskTimeoutError

    def __init__(self, tasks_queue, timeout, *,
                 logger=print,  # или lambda _: pass, если хочеться подавлять все ошибки
                 ):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super().__init__()
        self.queue = tasks_queue
        self.timeout = timeout
        self.logger = logger

    def run(self):
        """
        Старт работы воркера
        """
        signal(SIGALRM, TaskProcessor.timeout_handler)
        while True:
            task = self.queue.get()
            alarm(self.timeout)
            try:
                task.perform()
            except TaskProcessor.TaskTimeoutError:
                # pass
                self.logger("Timeout !")
            except Exception as e:
                alarm(0)   # Мало ли долго ждать работы логгера
                self.logger(e)   # (Печать, подавление, запись в файл или что захочется)
                return


class TaskManager(Process):
    """
    Мастер-процесс, который управляет воркерами
    """
    def __init__(self, tasks_queue, n_workers, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        super().__init__()
        self.queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.logger = print
        self.Tasks_Processors = []

    def run(self):
        """
        Запускайте бычка! (с)
        """
        self.Tasks_Processors = [TaskProcessor(self.queue,
                                               self.timeout,
                                               logger=self.logger) for _ in range(self.n_workers)]

        for proc in self.Tasks_Processors:
            proc.start()
        while True:
            # Обьяснений мне не дали, поэтому все работает в режиме демона
            for i in range(len(self.Tasks_Processors)):
                if not self.Tasks_Processors[i].proc.is_alive():
                    self.Tasks_Processors[i] = TaskProcessor(self.queue,
                                                             self.timeout,
                                                             logger=self.logger)
                    self.Tasks_Processors[i].start()

    def stop(self):
        for proc in self.Tasks_Processors:
            if proc.is_alive():
                proc.terminate()
        if self.is_alive():
            self.terminate()


"""
from random import randint
from time import time, sleep
from multiprocessing import Queue
t = 5
def func():
    a = time()
    _t = randint(1,t)
    print("_t = ",_t)
    sleep(_t)
    print(time() - a)

def main():
    queue = Queue()
    a = TaskManager(queue, 3, 2)
    a.start()
    n = 0
    while n < 10:
        queue.put(Task(func = func))
        n += 1
    sleep(10)


if __name__ == '__main__':
    main()

"""
