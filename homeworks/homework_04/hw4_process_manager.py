#!/usr/bin/env python
# coding: utf-8
from multiprocessing import Process, Manager, Event
from threading import Timer


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """

    def __init__(self, task, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать
        """
        self.args = args
        self.kwargs = kwargs
        self.task = task
        if 'ev' in kwargs:
            self.event = kwargs['ev']

    def perform(self, *args, **kwargs):
        """
        Старт выполнения задачи
        """
        event = kwargs.pop('ev')
        result = self.task(*args, **kwargs)
        event.set()
        return result


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, ev):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        task_obj = tasks_queue.get()

        task_obj.kwargs.update({'ev': ev})
        self.proc = Process(target=task_obj.perform,
                            args=task_obj.args, kwargs=task_obj.kwargs)

    def run(self):
        """
        Старт работы воркера
        """
        self.proc.start()


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
        print('start')
        self.tasks_queue = tasks_queue
        self.n_workers = n_workers
        self.timeout = timeout
        self.running_tasks = 0
        self.task_processors = []
        self.list_of_events = []

    def _check(self):
        while self.running_tasks < self.n_workers and not self.tasks_queue.empty():
            self.running_tasks += 1
            self.list_of_events.append(Event())
            self.task_processors.append(TaskProcessor(
                self.tasks_queue, self.list_of_events[-1]))
            self.task_processors[-1].run()

        flag = True
        if len(self.task_processors) == 0:
            print('end')
            flag = False

        i = 0
        for event in self.list_of_events:
            event.wait()
            self.running_tasks -= 1
            self.task_processors[i].proc.join()
            self.task_processors.pop(i)
            self.list_of_events.pop(i)
            i += 1

        if flag:
            self.run()

    def run(self):
        """
        Запускайте бычка! (с)
        """
        timer = Timer(0.01, self._check)
        timer.start()


def worker(a, b):
    result = a + b * 2
    print(result)
    return result


def olol(n):
    res = 0
    for i in range(n):
        res += i
    print(res)


manager = Manager()
que = manager.Queue()
que.put(Task(olol, 2 ** 25))
que.put(Task(olol, 2 ** 26))
que.put(Task(olol, 2 ** 27))

tm = TaskManager(que, 3, 100)
tm.run()
