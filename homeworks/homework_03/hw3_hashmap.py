#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class Entry:
        def __init__(self, key, value):
            """
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            """

        def get_key(self):
            # TODO возвращаем ключ
            raise NotImplementedError

        def get_value(self):
            # TODO возвращаем значение
            raise NotImplementedError

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            raise NotImplementedError

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        raise NotImplementedError

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        raise NotImplementedError

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        raise NotImplementedError

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        raise NotImplementedError

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        raise NotImplementedError

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        raise NotImplementedError

    def values(self):
        # TODO Должен возвращать итератор значений
        raise NotImplementedError

    def keys(self):
        # TODO Должен возвращать итератор ключей
        raise NotImplementedError

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        raise NotImplementedError

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        raise NotImplementedError

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        raise NotImplementedError

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        raise NotImplementedError
