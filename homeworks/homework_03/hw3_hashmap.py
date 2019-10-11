class HashMap:
    """
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    """

    class Iterator:

        def __iter__(self):
            return self

        def __init__(self, dict_, name):
            self.dict_ = dict_
            self.count_1 = 0
            self.count_2 = 0
            self.name = name

        def __next__(self):

            length = len(self.dict_)
            while self.count_1 < length:
                if len(self.dict_[self.count_1]) > 0:
                    if self.count_2 < len(self.dict_[self.count_1]):
                        item = self.dict_[self.count_1][self.count_2]
                        self.count_2 += 1
                        if self.name == 'keys':
                            return item.get_key()
                        elif self.name == 'values':
                            return item.get_value()
                        else:
                            return (item.get_key(), item.get_value())
                self.count_2 = 0
                self.count_1 += 1
            raise StopIteration

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
            # TODO реализовать функцию сравнения
            return self.key == other.get_key()

    def __init__(self, bucket_num=64):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.bucket_num = bucket_num
        self.dict_ = []
        for i in range(self.bucket_num):
            self.dict_.append([])
        self.num_of_items = 0
        self.bucket_use = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        index = self._get_index(self._get_hash(key))
        for i, element in enumerate(self.dict_[index]):
            if element.get_key() == key:
                return element.get_value()
        else:
            return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        item = self.Entry(key, value)
        index = self._get_index(self._get_hash(key))
        if not self.__contains__(key):
            self.num_of_items += 1
            if len(self.dict_[index]) == 0:
                self.bucket_use += 1
            self.dict_[index].append(item)
        else:
            for i, element in enumerate(self.dict_[index]):
                if element.get_key() == item.get_key():
                    self.dict_[index][i] = item
        if self.bucket_use / self.__len__() < 1.5:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self.num_of_items

    def _get_hash(self, key):
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        return self.Iterator(self.dict_, 'values')

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return self.Iterator(self.dict_, 'keys')

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        return self.Iterator(self.dict_, 'items')

    def _resize(self):
        self.num_of_items = 0
        array = []
        self.bucket_num *= 4
        for item in self.items():
            array.append(item)
        self.dict_ = []
        for i in range(self.bucket_num):
            self.dict_.append([])
        for i, element in enumerate(array):
            item = self.Entry(element[0], element[1])
            self.put(item.get_key(), item.get_value())

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        index = self._get_index(self._get_hash(item))
        for i, element in enumerate(self.dict_[index]):
            if element.get_key() == item:
                return True
