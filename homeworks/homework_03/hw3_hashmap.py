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
            return self.key == other.key

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.HMap = [[] for i in range(bucket_num)]
        self.bucket_num = bucket_num
        self.entry_num = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        if self.HMap[self._get_index(self._get_hash(key))]:
            for record in self.HMap[self._get_index(self._get_hash(key))]:
                if record.get_key() == key:
                    return record.get_value()
            if True:
                return default_value
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        new_record = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        its_new_key = True
        if self.HMap[index]:
            for p in range(len(self.HMap[index])):
                if new_record.__eq__(self.HMap[index][p]):
                    self.HMap[index][p] = new_record
                    its_new_key = False
                    break
            if its_new_key:
                self.HMap[index].append(new_record)
                self.entry_num += 1
        else:
            self.HMap[index].append(new_record)
            self.entry_num += 1

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.entry_num

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        curr_bucket = 0
        ind = 0
        while curr_bucket < self.bucket_num:
            if ind < len(self.HMap[curr_bucket]):
                yield self.HMap[curr_bucket][ind].get_value()
                ind += 1
            else:
                ind = 0
                curr_bucket += 1

    def keys(self):
        # TODO Должен возвращать итератор ключей
        curr_bucket = 0
        ind = 0
        while curr_bucket < self.bucket_num:
            if ind < len(self.HMap[curr_bucket]):
                yield self.HMap[curr_bucket][ind].get_key()
                ind += 1
            else:
                ind = 0
                curr_bucket += 1

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        curr_bucket = 0
        ind = 0
        while curr_bucket < self.bucket_num:
            if ind < len(self.HMap[curr_bucket]):
                yield (self.HMap[curr_bucket][ind].get_key(), self.HMap[curr_bucket][ind].get_value())
                ind += 1
            else:
                ind = 0
                curr_bucket += 1

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_size = 2 * self.bucket_num
        print('New size: ', new_size)
        values = self.items()
        new_hm = HashMap(new_size)
        for k, v in values:
            new_hm.put(k, v)
        self.HMap = new_hm.HMap
        self.bucket_num = new_size
        del new_hm

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: ' + str(self.bucket_num) + ', items: ' + str(self.entry_num)

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        if item in self.keys():
            return True
        if item in self.values():
            return True
        return False
