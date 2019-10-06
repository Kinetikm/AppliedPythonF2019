#!/usr/bin/env python
# coding: utf-8

from collections.abc import Iterator


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
            return

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
        self.length = 0
        self.bucket_num = bucket_num
        self.buckets = [[] for i in range(self.bucket_num)]
        return

    def get(self, key, default_value=None):
        entry = self._get_entry(key)
        if entry is not None:
            return entry.value

        return default_value

    def put(self, key, value):
        entry = self._get_entry(key)
        if entry is not None:
            entry.value = value
            return

        entry = HashMap.Entry(key, value)
        bucket_len = self._put_new_entry(entry)
        if bucket_len >= 10:
            self._resize()

        return

    def _put_new_entry(self, entry: Entry):
        """
        :param entry: hashmap entry
        :return: length is bucket
        """
        idx = self._get_index_by_key(entry.key)
        self.buckets[idx].append(entry)
        self.length += 1
        return len(self.buckets[idx])

    def _get_entry(self, key) -> Entry:
        for entry in self._get_block(key):
            if entry.key == key:
                return entry
        return None

    def _get_block(self, key) -> Entry:
        block = self.buckets[self._get_index_by_key(key)]
        return block

    def __len__(self):
        return self.length

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def _get_index_by_key(self, key):
        return self._get_index(self._get_hash(key))

    class HashMapIterator(Iterator):
        def __init__(self, hashmap, cursor=0, bucket_cursor=0, entity_transformer=lambda e: e):
            self._hashmap = hashmap
            self._cursor = cursor
            self._bucket_cursor = bucket_cursor
            self._entity_transformer = entity_transformer

            print('iterating over', hashmap)
            return

        def __next__(self):
            print("next", self._cursor, "bucket cursor", self._bucket_cursor)

            buckets = self._hashmap.buckets
            while(True):
                if self._cursor >= len(buckets):
                    raise StopIteration()

                print("len buckets:", len(buckets[self._cursor]))
                if self._bucket_cursor >= len(buckets[self._cursor]):
                    self._cursor += 1
                    self._bucket_cursor = 0
                    continue
                else:
                    break

            bucket = buckets[self._cursor]
            bucket_elem = bucket[self._bucket_cursor]
            print("bucket elen:", bucket_elem)
            elem = self._entity_transformer(bucket_elem)
            print("iterating elem:", elem)
            self._bucket_cursor += 1

            return elem

    def values(self):
        print("getting values")
        return HashMap.HashMapIterator(self, entity_transformer=lambda e: e.value)

    def keys(self):
        print("getting keys")
        return HashMap.HashMapIterator(self, entity_transformer=lambda e: e.key)

    def items(self):
        print("getting items")
        return HashMap.HashMapIterator(self, entity_transformer=lambda e: (e.key, e.value))

    def _resize(self):
        entries = [e for e in self.items()]
        self.bucket_num = self.bucket_num * 2
        self.buckets = [[] for i in range(self.bucket_num)]
        self.length = 0
        for k, v in entries:
            self.put(k, v)

        return

    def __str__(self):
        return "buckets: {}, items: {}".format(self.buckets, None)

    def __contains__(self, item):
        entry = self._get_entry(item)
        return entry is not None
