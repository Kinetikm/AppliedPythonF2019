#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, cpu_count
import time
import signal

# Замечание: В коде преднамеренно оставленно много дебаг кода


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
        if callable(task):
            self.task = task  # Функция, которую хотим выполнить
        else:
            raise TypeError
        self.args = args  # Позиционные параметры для функции
        self.kwargs = kwargs  # Именованные параметры для функции

    def perform(self):
        """
        Старт выполнения задачи
        """
        return self.task(*self.args, **self.kwargs)


class TaskProcessor(Process):
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, timeout):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        super(TaskProcessor, self).__init__()
        self.task_queue = tasks_queue
        self.timeout = timeout

    def run(self):
        """
        Старт работы воркера
        """

        def _handle_timeout(signum, frame):
            raise TimeoutError

        while True:
            signal.signal(signal.SIGALRM, _handle_timeout)  # Указываем какой сигнал хотим подать
            signal.alarm(self.timeout)  # Указываем через какое время будет подан сигнал
            try:
                task = self.task_queue.get()
                if task:
                    print(f"Процесс {self} взял задачу {task} в работу")
                    task.perform()
                    print(f"Задача {task} закончила работу ({task.__dict__})")
            except TimeoutError:
                try:
                    print(f"TIMEOUT Задача {task} не закончила работу ({task.__dict__})")
                    break
                except UnboundLocalError:
                    print(f"Задач больше нет")
            finally:
                signal.alarm(0)


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

    def run(self):
        active_task_processors = []

        while True:
            while len(active_task_processors) < self.n_workers:
                task_processor = TaskProcessor(self.tasks_queue, self.timeout)
                task_processor.start()
                active_task_processors.append(task_processor)

            for ind, active_task_processor in enumerate(active_task_processors):
                if not active_task_processor.is_alive():
                    active_task_processor.terminate()
                    print(f"Менеджер закончил процесс {active_task_processor}")
                    active_task_processors.pop(ind)


#  Блок тестов расположен в файле с программой, тк вы просили не трогать файл с тестами проекта
#  Можно было вынести их в отдельный файл, но зачем
#  Всё информацию о работе программы вывожу в терминал (можно было бы писать лог файл, но зачем)


def sleeper(sec, seconds=None):
    # print(f"Сплю {sec} секунд(ы)")
    time.sleep(sec)
    if seconds:
        # print(f"Сплю ещё {seconds} секунду")
        time.sleep(seconds)
    # print(f"Задача закончила работу {sec}, {seconds}")


def test1():
    queue = Manager().Queue()

    task1 = Task(sleeper, 2)
    task2 = Task(sleeper, 5, 1)
    task3 = Task(sleeper, 1, seconds=2)
    task4 = Task(sleeper, sec=0, seconds=1)
    task5 = Task(sleeper, 8, 4)
    task6 = Task(sleeper, 1, 9)

    queue.put(task1)
    queue.put(task2)
    queue.put(task3)
    queue.put(task4)
    queue.put(task5)
    queue.put(task6)

    manager = TaskManager(queue, 3, 4)
    manager.run()


def test2():  # В принципе проверяет тоже самое, что и test1
    import random

    queue = Manager().Queue()

    for i in range(10000):
        queue.put(Task(sleeper, random.randint(0, 10), random.randint(0, 10)))
        queue.put(Task(sleeper, sec=random.randint(0, 5), seconds=random.randint(0, 5)))

    manager = TaskManager(queue, cpu_count(), 10)
    manager.run()


test1()
# test2()
