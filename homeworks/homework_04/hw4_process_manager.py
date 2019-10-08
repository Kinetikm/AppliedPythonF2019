#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process


class Task:
    """
    Задача, которую надо выполнить.
    В идеале, должно быть реализовано на достаточном уровне абстракции,
    чтобы можно было выполнять "неоднотипные" задачи
    """
    def __init__(self, ...):
        """
        Пофантазируйте, как лучше инициализировать
        """
        raise NotImplementedError

    def perform(self):
        """
        Старт выполнения задачи
        """
        raise NotImplementedError


class TaskProcessor:
    """
    Воркер-процесс. Достает из очереди тасок таску и делает ее
    """
    def __init__(self, tasks_queue):
        """
        :param tasks_queue: Manager.Queue с объектами класса Task
        """
        raise NotImplementedError

    def run(self):
        """
        Старт работы воркера
        """
        raise NotImplementedError


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
        raise NotImplementedError

    def run(self):
        """
        Запускайте бычка! (с)
        """
        raise NotImplementedError
