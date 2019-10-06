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
            # raise NotImplementedError
            return self.key

        def get_value(self):
            # TODO возвращаем значение
            # raise NotImplementedError
            return self.value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            # raise NotImplementedError
            return self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        # raise NotImplementedError
        self.bucket_num = bucket_num
        self.bucket = [None] * self.bucket_num
        self.size_now = 0
        self.capacity = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        # raise NotImplementedError

        x = self._get_index(self._get_hash(key))
        if self.bucket[x] is None:
            return default_value
        for i in self.bucket[x]:
            if i.get_key() == key:
                return i.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        # raise NotImplementedError
        x = self._get_index(self._get_hash(key))
        if self.bucket[x] is None:
            self.bucket[x] = []
            self.capacity += 1
        k = True
        for i in self.bucket[x]:
            if i.get_key() == key:
                i.value = value
                k = False
        if k:
            self.bucket[x].append(self.Entry(key, value))
            self.size_now += 1

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        # raise NotImplementedError
        return self.size_now

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        # raise NotImplementedError
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        # raise NotImplementedError
        x = hash_value % self.bucket_num
        return x

    def values(self):
        # TODO Должен возвращать итератор значений
        for i in self.bucket:
            if i is not None:
                for j in i:
                    yield j.get_value()

    def keys(self):
        # TODO Должен возвращать итератор ключей
        for i in self.bucket:
            if i is not None:
                for j in i:
                    yield j.get_key()

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        # raise NotImplementedError
        for i in self.bucket:
            if i is not None:
                for j in i:
                    yield (j.get_key(), j.get_value())

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        # raise NotImplementedError
        k = 0.75
        if self.capacity >= self.bucket_num * k:
            for _ in range(self.bucket_num):
                self.bucket.append(None)

            self.bucket_num_new = self.bucket_num * 2

            for i, j in self.items():
                new_index = self._get_hash(i) % self.bucket_num_new
                index = self._get_index(self._get_hash(i))
                if new_index != index:
                    if self.bucket[new_index] is not None:
                        self.bucket[new_index].append(self.Entry(i, j))

                        for c in range(len(self.bucket[index])):
                            if self.bucket[index][c].get_key() == i:
                                del self.bucket[index][c]

                        if len(self.bucket[index][c]) == 0:
                            self.bucket[index][c] = None
                            self.capacity -= 1

                    else:
                        self.bucket[new_index] = [self.Entry(i, j)]
                        for c in range(len(self.bucket[index])):
                            if self.bucket[index][c].get_key() == i:
                                del self.bucket[index][c]
                        if len(self.bucket[index][c]) != 0:
                            self.capacity += 1
                        else:
                            self.bucket[index][c] = None
        self.bucket_num = self.bucket_num * 2

    def __str__(self):
        # # TODO Метод выводит "buckets: {}, items: {}"
        # # raise NotImplementedError
        print(f'buckets: {self.capacity}, items: {self.size_now}')

    def __contains__(self, item):
        if isinstance(item, self.Entry):
            x = self._get_index(self._get_hash(item.get_key()))
            for i in self.bucket[x]:
                if i == item:
                    return True
            return False
        else:
            x = self._get_index(self._get_hash(item))
            for i in self.bucket[x]:
                if i.get_key() == item:
                    return True
            return False

        # TODO Метод проверяющий есть ли объект (через in)
        # raise NotImplementedError
