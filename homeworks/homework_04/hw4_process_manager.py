#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, current_process
import time


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
        self.args = args
        self.kwargs = kwargs

    def perform(self):
        """
        Старт выполнения задачи
        """

        print(f'выполняется perform с args = {self.args}, kwargs = {self.kwargs}, имя процеса {current_process().name}')
        time.sleep(self.args[0])
        print(f"конец perform, времени для выполнения процесса {current_process().name}  хватило")


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks_queue = tasks_queue

    def run(self):
        """
        Старт работы воркера
        """

        if not self.tasks_queue.empty():
            item = self.tasks_queue.get()
            item.perform()


class TaskManager:
    """
    Мастер-процесс, который управляет воркерами
    """

    def __init__(self, tasks_queue, n_workers, timeout=None):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        :param n_workers: кол-во воркеров
        :param timeout: таймаут в секундах, воркер не может работать дольше, чем timeout секунд
        """
        self.n_workers = n_workers
        self.tasks_queue = tasks_queue
        self.tasks = [TaskProcessor(self.tasks_queue) for _ in range(self.n_workers)]
        self.timeout = timeout

    def run(self):
        """
        Запускайте бычка! (с)
        # """

        process_list = []
        if isinstance(self.timeout, int) or isinstance(self.timeout, float):
            for pr in self.tasks:
                x = Process(target=pr.run, args=())
                process_list.append(x)
            flag = True

            while not self.tasks_queue.empty():
                if flag:
                    for j in range(self.n_workers):
                        process_list[j].start()
                    flag = False

                else:
                    # отслеживается,чтобы количество рабочих процессов было n_worker
                    for j in range(self.n_workers):
                        if not process_list[j].is_alive():
                            process_list[j] = Process(target=self.tasks[j].run, args=())
                            process_list[j].start()

                start = time.time()
                # отслеживаем время работы процессов
                while time.time() - start <= self.timeout:
                    if any(process_list[j].is_alive() for j in range(self.n_workers)):
                        time.sleep(.1)
                    else:
                        break
                # если есть процессы, которые не закнчили работать, они убиваются
                for k in range(self.n_workers):
                    if process_list[k].is_alive():
                        process_list[k].terminate()
        elif self.timeout is None:
            for pr in self.tasks:
                x = Process(target=pr.run, args=())
                process_list.append(x)
                x.start()
            while not self.tasks_queue.empty():
                # пока очередь не пуста процессы будут обрабатывать ее, если какой то проесс умер, создается новый
                for j in range(self.n_workers):
                    if not process_list[j].is_alive():
                        process_list[j] = Process(target=self.tasks[j].run, args=())
                        process_list[j].start()
        else:
            raise ValueError


"""
Ниже приведен пример main, очередь состит из 1,2,3 ... 50 
в например perform прописано sleep(i)
если  задан timeout, тогда можно будет отслежить заботу алгоритма
если args[0]>timeout ,тогда не будет напечатана строчка print("конец perform, вермени хватило")

если timeout не задан(по умолчанию None), тогда можно будет увидеть, что результат выводится каждую секунду,
значит все выполняется с помощью разных процессов

"""

if __name__ == '__main__':
    tasks = []

    for i in range(20):
        tasks.append(Task(i))

    manager = Manager()
    queue1 = manager.Queue(20)

    for task in tasks:
        queue1.put(task)
    print(" TaskManager_with_timeout")
    TaskManager_with_timeout = TaskManager(tasks_queue=queue1, n_workers=4, timeout=5)
    TaskManager_with_timeout.run()

    queue2 = manager.Queue(20)

    for task in tasks:
        queue2.put(task)
    print("TaskManager_without_timeout ")
    TaskManager_without_timeout = TaskManager(tasks_queue=queue2, n_workers=4)
    TaskManager_without_timeout.run()
