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
            return self.key == other.get_key()

        def __iter__(self):
            yield self.key
            yield self.value

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.hash_map = [[] for i in range(int(self.bucket_num))]

    def get(self, key, default_value=None):
        index = self._get_index(self._get_hash(key))
        for entry in self.hash_map[index]:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value

    def put(self, key, value):
        index = self._get_index(self._get_hash(key))
        p_entry = self.Entry(key, value)
        for i, entry in enumerate(self.hash_map[index]):
            if entry == p_entry:
                self.hash_map[index].pop(i)
                break
        self.hash_map[index].append(p_entry)
        app = self.bucket_num * 0.75

        if len([lst for lst in self.hash_map if lst]) > app:
            self._resize()
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return len(self.items())

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return [entry.get_value() for entry in self.items()]

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return [entry.get_key() for entry in self.items()]

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return [entry for lst_of_entry in self.hash_map for entry in lst_of_entry]

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket_num *= 2
        items = self.items()
        self.hash_map = [[] for i in range(self.bucket_num)]
        for entry in items:
            self.put(entry.get_key(), entry.get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, len(self))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        return item in self.keys()
