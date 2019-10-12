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
        # Сами определяем функцию и кладём её в Таск
        self.func = func
        self.ar = args
        self.kwar = kwargs

    def perform(self, ans_dict, num):
        """
        Старт выполнения задачи
        """
        # Результат выполнения кладём в словарь(можно в очередь
        # num - номер Таска
        ans_dict[num] = self.func(*self.ar, **self.kwar)


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """

    def __init__(self, tasks_queue, num):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        self.tasks = tasks_queue
        self.num = num
        self.ans_dict = Manager().dict()

    def run(self):
        """
        Старт работы воркера
        """
        task = self.tasks.get()
        self.proc = Process(target=task.perform, args=(self.ans_dict, self.num))
        self.time = time.time()
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
        self.tasks = tasks_queue
        self.slaves = n_workers
        self.timeout = timeout
        self.working = True  # флажок

    def run(self):
        """
        Запускайте бычка! (с)
        """
        result = dict()  # словарь с результатами выполнения Тасков
        chislo_rabotyag = 0  # отвечает за количество работающих воркеров
        tsk_done = 0  # Номер Таска (для передачи в дальнейшие функции и запись в словарь с результатами)
        rabotyagi = dict()  # Тут хранятся воркеры для быстрого доступа к ним (можно было использовать обычный лист)
        start_time = time.time()
        while (self.working):
            #  пока ативен флажок
            if (self.tasks.empty()) and (chislo_rabotyag == 0):  # нет тасков и работающих воркеров
                start_time = time.time()  # для своевременного отключения
            while (self.tasks.empty()) and (len(rabotyagi) == 0):  # нет тасков и работающих воркеров
                if time.time() - start_time > 5:  # если время ожидания велико, то отключаемся
                    self.working = False
                    break
                print('wait for tasks')
                time.sleep(1)
            while (chislo_rabotyag < self.slaves) and (not self.tasks.empty()):  # если есть свободные работяги и работа
                print('new process open')
                rabotyagi[tsk_done] = TaskProcessor(self.tasks, tsk_done)
                rabotyagi[tsk_done].run()
                chislo_rabotyag += 1
                tsk_done += 1
            keys = list(rabotyagi.keys())
            for key in keys:
                if not rabotyagi[key].proc.is_alive():  # выключение завершённых процессов
                    print('process close')
                    result.update(rabotyagi[key].ans_dict)
                    rabotyagi[key].proc.join()
                    rabotyagi.pop(key)
                    chislo_rabotyag -= 1
                elif (time.time() - rabotyagi[key].time) > self.timeout:  # выключение долгих процессов
                    print('process close cause of time is up')
                    result.update({key: "time is up"})
                    rabotyagi[key].proc.terminate()
                    rabotyagi.pop(key)
                    chislo_rabotyag -= 1

        return result


# ну а тут всякие тестики
'''def sum(a, b):  # функция с принтом
    print(a + b)


def timesum(a, b):  # с задержкой
    time.sleep(5)
    return a + b


def mul(a, b):  # просто функция с результатом
    return a * b


task1 = Task(sum, *[1, 2])
task2 = Task(mul, *[4, 7])
task3 = Task(sum, *[10, 20])
task4 = Task(timesum, *[4, 5])
task5 = Task(sum, *[100, 200])


def adding(n, queue):  # функция для добавления Тасков в очередь (реализуется через другой процесс)
# Не знаю как реализовать добавление Тасков в очередь одновременно с работающим менеджером в одном процессе
# вряд ли это возможно (возможно, но не реалистично, да и не особо красиво)
    for i in range(n):
        queue.put(Task(mul, *[i, i]))
        queue.put(Task(timesum, *[4, 5]))


if __name__ == "__main__":
    tsk_qu = Manager().Queue()
    subproc = Process(target=adding, args=(5, tsk_qu)) #
    subproc.start()
    m = TaskManager(tsk_qu, 3, 1)
    an = m.run()
    subproc.join()
    print(an)'''
