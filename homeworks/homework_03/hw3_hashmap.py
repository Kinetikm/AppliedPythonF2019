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
        self._bucket = [[] for i in range(int(self.length))]
        self.free_place = 0.66

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for var in self._bucket[index]:
            if var.key == key:
                default_value = var.value
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        if key not in self.keys():
            index = self._get_index(self._get_hash(key))
            self._bucket[index].append(self.Entry(key, value))
        else:
            index = self._get_index(self._get_hash(key))
            if self._bucket[index]:
                for var in self._bucket[index]:
                    if var.key == key:
                        var.value = value
        if (len([lst for lst in self._bucket if lst]) / self.length) > self.free_place:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return len(self.items())

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
        return [ent for lst_of_ent in self._bucket for ent in lst_of_ent]

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.length *= 2
        items = self.items()
        self._bucket = [[] for i in range(self.length)]
        for ent in items:
            self.put(ent.get_key(), ent.get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
