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
            self._key = key
            self._value = value

        def get_key(self):
            '''
            Возвращает ключ
            '''
            return self._key

        def get_value(self):
            '''
            Возвращает значение
            '''
            return self._value

        def __eq__(self, other):
            '''
            Сравнивает два ключа
            :param other: другой объект Entry
            '''
            return self._key == other.get_key()

    class Iterator:
        def __init__(self, table, type_):
            '''
            Итератор по ключам таблицы
            :param table: лист листов, в котором хранятся Entry
            '''
            self.pointer_1 = 0
            self.pointer_2 = 0
            self.table = []
            self.type_ = type_
            for item in table:
                if item:
                    self.table.append(item)

        def return_this_type(self, pointer_1, pointer_2):
            if self.type_ == 'key':
                return self.table[self.pointer_1][self.pointer_2].get_key()
            elif self.type_ == 'value':
                return self.table[self.pointer_1][self.pointer_2].get_value()
            elif self.type_ == 'item':
                key = self.table[self.pointer_1][self.pointer_2].get_key()
                value = self.table[self.pointer_1][self.pointer_2].get_value()
                return (key, value)

        def __iter__(self):
            return self

        def __next__(self):
            if self.pointer_1 < len(self.table):
                if len(self.table[self.pointer_1]) == 1:
                    self.pointer_2 = 0
                    item = self.return_this_type(self.pointer_1, self.pointer_2)
                    self.pointer_1 += 1
                    return item
                else:
                    if self.pointer_2 < len(self.table[self.pointer_1]):
                        item = self.return_this_type(self.pointer_1, self.pointer_2)
                        self.pointer_2 += 1
                        return item
                    else:
                        self.pointer_1 += 1
                        if self.pointer_1 < len(self.table):
                            self.pointer_2 = 0
                            item = self.return_this_type(self.pointer_1, self.pointer_2)
                            return item
                        else:
                            raise StopIteration
            else:
                raise StopIteration

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self._bucket_num = bucket_num
        self._num_nodes = 0  # количество Entry в массиве
        self._table = [[] for _ in range(self._bucket_num)]  # задаем начальную пустую таблицу
        self._LOAD_COEFF = 0.66  # коэффициент заполнения (2/3)
        self._COEFF = 4  # во сколько раз будем увеличивать размер таблицы

    def get(self, key, default_value=None):
        '''
        Возвращает значение по ключу
        Если оно присутствует, возвращаем default_value
        :param key: ключ
        :param default_value: дефолтное значение
        '''
        # индекс ячейки, в которой будем искать элемент
        idx = self._get_index(self._get_hash(key))
        # если в ячейке ничего нет, то возвращаем дефолт
        # если в ячейке, что-то есть, то пытаемся найти элемент, сравнивая ключи
        # если такого ключа нет, то возвращаем дефолт
        if not self._table[idx]:
            return default_value
        for elem in self._table[idx]:
            if key == elem.get_key():
                return elem.get_value()
        return default_value

    def put(self, key, value):
        '''
        Кладет значение по ключу
        В случае, если ключ уже присутствует он его заменяет
        :param key: ключ
        :param value: значение
        '''
        # индекс ячейки, в которую будем класть элемент
        idx = self._get_index(self._get_hash(key))
        node = self.Entry(key, value)
        # если ячейка пустая, то просто кладем элемент
        # если ячейка не пустая, то проверяем, есть ли искомый ключ
        # если ключ есть, то заменяем, если нет, то кладем в конец листа
        if not self._table[idx]:
            self._table[idx].append(node)
            self._num_nodes += 1
            return
        if self.__contains__(key):
            for i in range(len(self._table[idx])):
                if node == self._table[idx][i]:
                    self._table[idx][i] = node
                    if self._num_nodes > self._LOAD_COEFF * self._bucket_num:
                        self._resize()
                    return
        else:
            self._table[idx].append(node)
            self._num_nodes += 1
            if self._num_nodes > self._LOAD_COEFF * self._bucket_num:
                self._resize()
            return

    def __len__(self):
        '''
        Возвращает количество Entry в массиве
        '''
        return self._num_nodes

    def _get_hash(self, key):
        '''
        Возвращает хэш от ключа
        :param key: ключ
        '''
        return hash(key)

    def _get_index(self, hash_value):
        '''
        По значению хеша возвращаем индекс элемента в массиве
        :param hash_value: хэш от ключа
        '''
        return hash_value % self._bucket_num

    def values(self):
        '''
        Возвращает итератор значений
        '''
        return self.Iterator(self._table, type_='value')

    def keys(self):
        '''
        Возвращает итератор ключей
        '''
        return self.Iterator(self._table, type_='key')

    def items(self):
        '''
        Возвращает итератор пар ключ и значение (tuples)
        '''
        return self.Iterator(self._table, type_='item')

    def _resize(self):
        '''
        Увеличивает количество бакетов и перестраивать таблицу
        '''
        items = [item for item in self.items()]
        self._bucket_num *= self._COEFF
        num_elements_save = self._num_nodes
        del self._table
        self._table = [[] for _ in range(self._bucket_num)]
        for key, value in items:
            self.put(key, value)
        self._num_nodes = num_elements_save

    def __str__(self):
        '''
        Метод выводит "buckets: {}, items: {}"
        '''
        return 'buckets: {}, items: {}'.format(self._bucket_num, self._num_nodes)

    def __contains__(self, item):
        '''
        Метод проверяющий есть ли объект (через in)
        '''
        for key in self.keys():
            if item == key:
                return True
