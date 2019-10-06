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
            self.key = key
            self.value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.length = bucket_num
        self._bucket = [None for i in range(self.length)]
        self.capacity = 0
        self.free_place = 0.66

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        if self._bucket[index] is not None:
            for var in self._bucket[index]:
                if var.key == key:
                    default_value = var.value
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        if key not in self.keys():
            index = self._get_index(self._get_hash(key))
            if self._bucket[index] is None:
                self._bucket[index] = [self.Entry(key, value)]
            else:
                self._bucket[index].append(self.Entry(key, value))
            self.capacity += 1
        else:
            index = self._get_index(self._get_hash(key))
            if self._bucket[index]:
                for var in self._bucket[index]:
                    if var.key == key:
                        var.value = value
        if self.capacity / self.length > self.free_place:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.capacity

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.length

    def values(self):
        # TODO Должен возвращать итератор значений
        return list(map(lambda x: x[1], self.items()))

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return list(map(lambda x: x[0], self.items()))

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        result = []
        for bucket in self._bucket:
            if bucket:
                for var in bucket:
                    result.append((var.key, var.value))
        return result

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.length *= 2
        tmp_buckets = []
        for bucket in self._bucket:
            for entry in bucket:
                tmp_buckets.append(entry)
            self._bucket = [None for i in range(self.length)]
        for entry in tmp_buckets:
            self.put(entry.key, entry.value)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return f"buckets: {self._bucket}, items: {self.items()}"

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
