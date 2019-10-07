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
            self._key = key
            self._value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self._key

        def get_value(self):
            # TODO возвращаем значение
            return self._value

        def set_value(self, value):
            self._value = value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self._key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._arr = [[]] * bucket_num
        self._size = bucket_num
        self._length = 0
        self._coefficient = 2 / 3

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for elem in self._arr[index]:
            if elem.get_key() == key:
                return elem.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        index = self._get_index(self._get_hash(key))
        for item in self._arr[index]:
            if item.get_key() == key:
                item.set_value(value)
                return
        self._arr[index].append(self.Entry(key, value))
        self._length += 1
        if self._length > self._size * self._coefficient:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._length

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._size

    def values(self):
        # TODO Должен возвращать итератор значений
        return (elem.get_value() for bucket in self._arr for elem in bucket)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (elem.get_key() for bucket in self._arr for elem in bucket)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return ((elem.get_key(), elem.get_value()) for bucket in self._arr for elem in bucket)

    def _resize(self):
        temp = HashMap(bucket_num=self._size * 4)
        for key, value in self.items():
            temp.put(key, value)
        self.__dict__.update(temp.__dict__)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self._size, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for elem in self._arr[index]:
            if elem.get_key() == item:
                return True
        return False
