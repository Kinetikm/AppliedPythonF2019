#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process
import time


class Task:
    """
    Задача, которую надо выполнить.
    """
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """
        self._func(*self._args, **self._kwargs)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, queue):
        """
        :param queue: Manager.Queue с объектами класса Task
        """
        task = queue.get()
        if not isinstance(task, Task):
            raise TypeError('unexpected object in task_queue, object of Task class expected')
        self.task = task
        self.time = None
        self.proc = None

    def run(self):
        """
        Старт работы воркера
        """
        self.proc = Process(target=self.task.perform)
        self.proc.start()
        self.time = time.time()


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
        self._n_workers = n_workers
        self._timeout = timeout
        self.delay = self._timeout / 5 / self._n_workers  # нужно провереть состояние воркеров не сильно часто, чтобы
        #  позволять им работать без излишних переключений между процессами, но несколько раз за время до таймаута;
        #  чем больше воркеров тем чаще один из них будет заканчивать задачу -> чаще проверяем

    def run(self):
        """
        Запускайте бычка! (с)
        """

        jobs = self._workers_init()
        while not self._queue.empty():
            i = 0
            proc_to_del = []
            if not jobs[i].proc.is_alive():
                proc_to_del.append(i)
            elif time.time() - jobs[i].time > self._timeout:
                print('Timeout on task {}'.format(jobs[i].task))
                jobs[i].proc.terminate()
                jobs[i].proc.join()
                proc_to_del.append(i)
            jobs = self._del_process(proc_to_del, jobs)
            time.sleep(self.delay)
        self.stop(jobs)

    def _workers_init(self):
        """создает набор TaskProcessor и запускает их"""
        jobs = []
        for _ in range(self._n_workers):
            task = TaskProcessor(self._queue)
            jobs.append(task)
            task.run()
        return jobs

    def _del_process(self, proc_to_del, jobs):
        """удаляет завершившееся TaskProcessor из списка активных и создает и запускает вместо них новые"""
        jobs = [i for j, i in enumerate(jobs) if j not in proc_to_del]
        for _ in range(self._n_workers - len(jobs)):
            task = TaskProcessor(self._queue)
            jobs.append(task)
            task.run()
        return jobs

    def stop(self, jobs):
        """ждет завершения работающих TaskProcessor"""
        while len(jobs) != 0:
            proc_to_del = []
            for i in range(len(jobs)):
                if not jobs[i].proc.is_alive():
                    proc_to_del.append(i)
                elif time.time() - jobs[i].time > self._timeout:
                    print('Timeout on task {}'.format(jobs[i].task))
                    jobs[i].proc.terminate()
                    jobs[i].proc.join()
                    proc_to_del.append(i)
            jobs = [i for j, i in enumerate(jobs) if j not in proc_to_del]
            time.sleep(self.delay)
