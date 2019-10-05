#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class ItemIterator:
        def __init__(self, hash_map, keys):
            self._position = 0
            self._keys = keys
            self._hash_map = hash_map

        def __iter__(self):
            return self

        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            key = self._keys[self._position]
            value = self._hash_map.get(key)
            self._position += 1
            return (key, value)

    class KeyIterator(ItemIterator):
        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            self._position += 1
            return self._keys[self._position - 1]

    class ValueIterator(ItemIterator):
        def __next__(self):
            if self._position == len(self._keys):
                raise StopIteration
            self._position += 1
            return self._hash_map.get(self._keys[self._position - 1])

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
            # возвращаем ключ
            return self._key

        def get_value(self):
            # возвращаем значение
            return self._value

        def __eq__(self, other):
            # функция сравнения
            return self._key == other.get_key()

        def set_value(self, value):
            self._value = value

    def __init__(self, bucket_num=64, coef_for_resize=0.85):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._bucket_num = bucket_num
        self._len = 0
        self._hash_map = [[] for _ in range(0, self._bucket_num)]
        self._coef_for_resize = coef_for_resize
        self._bucket_counts = 0
        self._list_of_keys = []

    def get(self, key, default_value=None):
        #  метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        idx = self._get_index(self._get_hash(key))
        bucket = self._hash_map[idx]
        for entry in bucket:
            if key == entry.get_key():
                return entry.get_value()
        return default_value

    def put(self, key, value):
        #  метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        idx = self._get_index(self._get_hash(key))
        bucket = self._hash_map[idx]
        if key not in [entry.get_key() for entry in bucket]:
            bucket.append(self.Entry(key, value))
            self._len += 1
            self._list_of_keys.append(key)
            if len(bucket) == 0:
                self._bucket_counts += 1
        else:
            for i in range(0, len(bucket)):
                if bucket[i].get_key() == key:
                    bucket[i].set_value(value)
        if len(self) > self._bucket_num * self._coef_for_resize:
            self._resize()

    def __len__(self):
        # Возвращает количество Entry в массиве
        return self._len

    def _get_hash(self, key):
        #  Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # По значению хеша вернуть индекс элемента в массиве
        return hash_value % self._bucket_num

    def values(self):
        # Возвращает итератор значений
        return self.ValueIterator(self, self._list_of_keys)

    def keys(self):
        # Возвращаet итератор ключей
        return self.KeyIterator(self, self._list_of_keys)

    def items(self):
        # Возвращает итератор пар ключ и значение (tuples)
        return self.ItemIterator(self, self._list_of_keys)

    def _resize(self):
        # Время от времени нужно ресайзить нашу хешмапу
        new_bucket_num = 2*self._bucket_num
        items = self.items()
        new_hash_map = HashMap(bucket_num=new_bucket_num)
        for item in items:
            new_hash_map.put(item[0], item[1])
        self.__dict__.update(new_hash_map.__dict__)

    def __str__(self):
        # Метод выводит "buckets: {}, items: {}"
        return f'bucket: {self._bucket_num}, items: {self._len}'

    def __contains__(self, key):
        # Метод проверяющий есть ли объект (через in)
        # :)
        idx = self._get_index(self._get_hash(key))
        for entry in self._hash_map[idx]:
            if entry.get_key() == key:
                return True
        return False
