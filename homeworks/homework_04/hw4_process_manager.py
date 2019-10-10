#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process
import time


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, func, ret, *args, **kwargs):
        """
        Пофантазируйте, как лучше инициализировать

        """
        '''
        вообще по хорошему надо бы среди инициализирующих параметров как-нибудь передавать опциональную перемнную ret,
        отвечающую за то, куда мы будем возвращать результат функции, если её выполним. А может, и не надо
        хотя эту самую переменную можно будет передавать как список, и тогда её можно будет изменить внутри воркера, таким образом
        передав через неё результат функции наружу, ведь так?
        
        
        '''
        self._func = func
        self._args = args # may be self._args = args or None???
        self._kwargs = kwargs or None # same here as above

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self._func(self._args, self._kwargs) # что если args, kwargs = None???


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self._task = tasks_queue.get()
        self.busy = False # параметр, определяющий, занят ли сейчас воркер или ничего не делает
        self._in_process = None

    def run(self):
        """
        Старт работы воркера
        """
        self.busy = True
        self._in_process = Process(target=self._task.perform())
        self._in_process.start()
        self._in_process.join()
        self.busy = False

    def terminate(self, tasks_queue=None):
        self._in_process.terminate()
        self.busy = False
        if tasks_queue is not None:
            self._task = tasks_queue.get()
            self.run()

    def wake(self, tasks_queue):
        self._task = tasks_queue.get()
        self.run()


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
        self._tasks_queue = tasks_queue
        self._n_workers = n_workers
        self._timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        """
        '''# worker's state dict unit: {worker_id: start_time}
        workers_states = {}
        for i in range(self._n_workers):
            workers_states[i] = [0]
        # как вариант хранить все процессы в очереди, либо менять их id в зависимости от времени создания, чтобы в
        # начале дикта лежали самые старые процессы
        # далее приведу реализацию для списка типа очередь
        # элемент списка - список [worker_id, start_time]
        '''
        workers = [[i, None, None] for i in range(self._n_workers)]
        while True:
            for worker in workers:
                if self._tasks_queue.epmty():
                    return
                if worker[1] is None:
                    worker_id = worker[0]
                    workers.remove(worker)
                    new_worker = TaskProcessor(self._tasks_queue)
                    workers.append([worker_id, new_worker, time.clock()])
                    new_worker.run()
                elif not worker[1].busy:
                    worker[1].wake(tasks_queue)
                    worker[2] = time.clock()
                elif time.clock() - worker[2] > self._timeout:
                    worker[1].terminate(self._tasks_queue)
                    worker[2] = time.clock()
