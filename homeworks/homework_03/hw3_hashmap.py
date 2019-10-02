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
            return self.key

        def get_value(self):
            return self.value

        def __eq__(self, other):
            return self.key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.length = 0
        self.bucket_num = bucket_num
        self.bucket = [[] for _ in range(bucket_num)]

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = hash(key) % self.bucket_num
        entries = self.bucket[ind]

        if entries:
            for ent in entries:
                if key == ent.get_key():
                    return ent.get_value()

        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет

        ind = hash(key) % self.bucket_num
        entries = self.bucket[ind]

        if entries:
            for ent in entries:
                if key == ent.get_key():
                    ent.value = value
                    return

        self.length += 1
        entries.append(self.Entry(key, value))

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.length

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    class ItemIter:
        def __init__(self, hashmap, mode):
            self.index = 0
            self.values = []
            for buck in hashmap.bucket:
                if not buck:
                    continue
                for ent in buck:
                    if mode == 0:
                        self.values.append(ent.get_value())
                    elif mode == 1:
                        self.values.append(ent.get_key())
                    else:
                        self.values.append(tuple((ent.get_key(), ent.get_value())))

        def __iter__(self):
            return self

        def __next__(self):
            if self.index == len(self.values):
                raise StopIteration
            value = self.values[self.index]
            self.index += 1
            return value

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.ItemIter(self, 0)

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.ItemIter(self, 1)

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.ItemIter(self, 2)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        self.bucket += [[] for _ in range(self.bucket_num)]
        self.bucket_num *= 2

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        items = [str(it) for it in self.items()]
        return "buckets: {}, items: {}".format(self.length, ", ".join(items))

    def __contains__(self, item):
        ind = hash(item) % self.bucket_num
        entries = self.bucket[ind]
        print(item)
        for ent in entries:
            if item == ent.get_key():
                return True
        return False
