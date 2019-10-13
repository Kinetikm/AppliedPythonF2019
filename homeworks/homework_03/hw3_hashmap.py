#!/usr/bin/env python
# coding: utf-8


class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """
    class ItemIterator:

        def __init__(self, hashmap):
            self.limit = hashmap._table_size
            self._cursor = 0
            self.buckets = hashmap._buckets
            # cached vars
            self.c_entries = []
            self.c_cursor = 0

        def __iter__(self):
            return self

        def __next__(self):
            while self._cursor < self.limit:
                # print(self._cursor, len(self.buckets))
                entries = self.buckets[self._cursor]

                if len(entries) > 1:
                    if not self.c_entries:
                        for entry in entries:
                            self.c_entries.append(entry)

                elif len(entries) == 1:
                    self._cursor += 1
                    k = entries[self.c_cursor - 1].get_key()
                    v = entries[self.c_cursor - 1].get_value()
                    return (k, v)

                if self.c_entries:
                    if self.c_cursor < len(self.c_entries):
                        self.c_cursor += 1
                        k = self.c_entries[self.c_cursor - 1].get_key()
                        v = self.c_entries[self.c_cursor - 1].get_value()
                        return (k, v)
                    else:
                        self.c_entries = []
                        self.c_cursor = 0
                        self._cursor += 1
                else:
                    self._cursor += 1
            raise StopIteration

    class KeyIterator(ItemIterator):

        def __next__(self):
            while self._cursor < self.limit:

                entries = self.buckets[self._cursor]

                if len(entries) > 1:
                    if not self.c_entries:
                        for entry in entries:
                            self.c_entries.append(entry)

                elif len(entries) == 1:
                    self._cursor += 1
                    return entries[0].get_key()

                if self.c_entries:
                    if self.c_cursor < len(self.c_entries):
                        self.c_cursor += 1
                        return self.c_entries[self.c_cursor - 1].get_key()
                    else:
                        self.c_entries = []
                        self.c_cursor = 0
                        self._cursor += 1
                else:
                    self._cursor += 1
            raise StopIteration

    class ValueIterator(ItemIterator):

        def __next__(self):
            while self._cursor < self.limit:
                entries = self.buckets[self._cursor]

                if len(entries) > 1:
                    if not self.c_entries:
                        for entry in entries:
                            self.c_entries.append(entry)

                elif len(entries) == 1:
                    self._cursor += 1
                    return entries[0].get_value()

                if self.c_entries:
                    if self.c_cursor < len(self.c_entries):
                        self.c_cursor += 1
                        return self.c_entries[self.c_cursor - 1].get_value()
                    else:
                        self.c_entries = []
                        self.c_cursor = 0
                        self._cursor += 1
                else:
                    self._cursor += 1
            raise StopIteration

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
            return self._key

        def set_value(self, value):
            self._value = value

        def get_value(self):
            return self._value

        def __eq__(self, other):
            return self.get_key() == other.get_key()

        def __repr__(self):
            return str((self._key, self._value))

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._table_size = bucket_num
        self._buckets = [[] for _ in range(self._table_size)]
        self._num_of_elements = 0

    def get(self, key, default_value=None):
        i = self._get_index(self._get_hash(key))
        entries = self._buckets[i]
        for entry in entries:
            if entry.get_key() == key:
                return entry.get_value()
        return default_value

    def put(self, key, value):
        i = self._get_index(self._get_hash(key))
        old_entries = self._buckets[i]
        new_entry = self.Entry(key, value)
        for old_entry in old_entries:
            if old_entry.get_key() == new_entry.get_key():
                new_value = new_entry.get_value()
                old_entry.set_value(new_value)
                return

        old_entries.append(new_entry)
        self._num_of_elements += 1

        if self._num_of_elements > 2 * self._table_size / 3:
            self._resize()

    def __len__(self):
        return self._num_of_elements

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self._table_size

    def values(self):
        val_it = self.ValueIterator(self)
        return val_it

    def keys(self):
        key_it = self.KeyIterator(self)
        return key_it

    def items(self):
        item_it = self.ItemIterator(self)
        return item_it

    def _resize(self):
        hash_items = self.items()
        self._table_size *= 2
        self._buckets = [[] for _ in range(self._table_size)]
        self._num_of_elements = 0
        for key, value in hash_items:
            self.put(key, value)

    def __str__(self):
        return 'buckets: {}, items: {}'.format(self._table_size, self._num_of_elements)

    def __contains__(self, key):
        for h_keys in self.keys():
            if h_keys == key:
                return True
        return False
