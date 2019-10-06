#!/usr/bin/env python
# coding: utf-8


class HashMap:

    class Entry:

        def __init__(self, key, value):
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
            if not isinstance(other, HashMap.Entry):
                return False
            elif self.key == other.key:
                return True
            return False

    def __init__(self, bucket_num=64):
        self.entry_list = [[] for i in range(bucket_num)]
        self.bucket_num = bucket_num

    def get(self, key, default_value=None):
        if self.entry_list[hash(key) % self.bucket_num] != []:
            for ent in self.entry_list[hash(key) % self.bucket_num]:
                if ent.key == key:
                    return ent.value
        return default_value

    def put(self, key, value):
        entry = self.Entry(key, value)
        if self.entry_list[hash(key) % self.bucket_num] != []:
            for ent in self.entry_list[hash(key) % self.bucket_num]:
                if ent.key == key:
                    self.entry_list[hash(key) % self.bucket_num].remove(ent)
                    break
        self.entry_list[hash(key) % self.bucket_num] += [entry]

    def __len__(self):
        return len(self.items())

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.bucket_num

    def values(self):
        value_list = []
        for bucket in self.entry_list:
            for ent in bucket:
                value_list += [ent.value]
        return value_list

    def keys(self):
        key_list = []
        for bucket in self.entry_list:
            for ent in bucket:
                key_list += [ent.key]
        return key_list

    def items(self):
        item_list = []
        for bucket in self.entry_list:
            for ent in bucket:
                item_list += [(ent.key, ent.value)]
        return item_list

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_self = HashMap(self.bucket_num*2)
        for ent in self.items():
            new_self.put(ent[0], ent[1])
        self = new_self

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        hashmap_str = 'buckets: '
        n_buc = 0
        for bucket in self.entry_list:
            if bucket != []:
                n_buc += 1
        hashmap_str += str(n_buc) + ', items: ' + str(len(self.items()))
        return hashmap_str

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        # print(item)
        for ent in self.entry_list[hash(item) % self.bucket_num]:
            if ent.key == item:
                return True
        else:
            return False
