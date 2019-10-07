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
            raise NotImplementedError

        def get_value(self):
            return self.value
            raise NotImplementedError

        def __eq__(self, other):
            if self.key == other:
                return True
            else:
                return False
            raise NotImplementedError
            
    class Iterator:
        def __init__(self, table, name):
            self.table = table
            self.name = name
            self.num1 = 0
            self.num2 = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            while self.num1 <  len(self.table):
                print(self.num1)
                #print(self.num1)
                #print(len(self.table))
                if len(self.table[self.num1]) > 0:
                    if len(self.table[self.num1]) > self.num2:
                        if self.name == "keys":
                            num2 = self.num2
                            self.num2 += 1
                            return self.table[self.num1][num2].get_key()
                        elif self.name == "values":
                            num2 = self.num2
                            self.num2 += 1
                            return self.table[self.num1][num2].get_value()
                        elif self.name == "items":
                            num2 = self.num2
                            self.num2 += 1
                            return (self.table[self.num1][num2].get_key(), self.table[self.num1][num2].get_value())
                self.num2 = 0
                self.num1 += 1

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.num  = bucket_num
        self.table = [[] for i in range(self.num)]
        self.num_of_items = 0
        self.filled_cells = 0;

    def get(self, key, default_value=None):
        if not self.__contains__(key):
            return default_value
        i = self._get_index(self._get_hash(key))
        for j in self.table[i]:
            if j.get_key() == key:
                return j.get_value()

    def put(self, key, value):
        i = self._get_index(self._get_hash(key))
        if self.__contains__(key):
            for j in self.table[i]:
                if j.__eq__(key):
                    j.value = value
                    return
        if len(self.table[i]) == 0:
               self.filled_cells += 1
        self.table[i].append(self.Entry(key, value))
        self.num_of_items += 1
        if self.num_of_items > 0.66 * self.num:
            self.resize()

    def __len__(self):
        return self.num_items

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        return hash_value % self.num

    def values(self):
        return self.Iterator(self.table, "values")
        raise NotImplementedError

    def keys(self):
        return self.Iterator(self.table, "keys")
        raise NotImplementedError

    def items(self):
        return self.Iterator(self.table, "items")
        raise NotImplementedError

    def _resize(self):
        table = self.table[:]
        self.num = 2 * self.num
        self.table = [[] for i in range(self.num)]
        for i in table:
            for j in i:
                self.put(j.key, j.value)
        raise NotImplementedError

    def __str__(self):
        return "buckets: {0}, items: {1}".format(self.filled_cells, self.num_of_items)
        raise NotImplementedError

    def __contains__(self, item):
        i = self._get_index(self._get_hash(item))
        for j in self.table[i]:
            if j.get_key() == item:
               return True
        return False
        raise NotImplementedError
