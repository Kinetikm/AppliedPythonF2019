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
            """
            Возвращает ключ
            """
            return self.key

        def get_value(self):
            """
            Возвращает значение
            """
            return self.value

        def __eq__(self, other):
            """
            Сравнивает объекты по ключу
            :param other:
            """
            return isinstance(other, type(self)) and self.key == other.get_key()

    def __init__(self, bucket_num=64, coef_for_resize=0.9):
        """
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        """
        self.hash_table = [None for i in range(bucket_num)]
        self.bucket_num = bucket_num
        self.coef_res = coef_for_resize

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        ind = self._get_index(self._get_hash(key))
        if self.hash_table[ind] is not None:
            for entry in self.hash_table[ind]:
                if entry.get_key() == key:
                    return entry.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет
        ind = self._get_index(self._get_hash(key))
        item = self.Entry(key, value)
        if self.hash_table[ind] is None:
            self.hash_table[ind] = [item]
            return
        for i, elem in enumerate(self.hash_table[ind]):
            if elem.get_key() == key:
                self.hash_table[ind][i] = item
                return
        self.hash_table[ind] += [item]
        if self.__len__() / self.bucket_num > self.coef_res:
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        length = 0
        for i in self.hash_table:
            if i is not None:
                length += len(i)
        return length

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % self.bucket_num

    def values(self):
        # TODO Должен возвращать итератор значений
        for i in self.hash_table:
            if i is not None:
                for j in i:
                    yield j.get_key()

    def keys(self):
        # TODO Должен возвращать итератор ключей
        for i in self.hash_table:
            if i is not None:
                for j in i:
                    yield j.get_value()

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        for i in self.hash_table:
            if i is not None:
                for j in i:
                    yield (j.get_key(), j.get_value())

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        new_bucket_num = 2 * self.bucket_num
        items = self.items()
        new_hash_map = HashMap(bucket_num=new_bucket_num)
        for item in items:
            new_hash_map.put(item[0], item[1])
        self.__dict__.update(new_hash_map.__dict__)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return 'buckets: {}, items: {}'.format(self.bucket_num, self.__len__())

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        ind = self._get_index(self._get_hash(item))
        if self.hash_table[ind] is not None:
            for i in self.hash_table[ind]:
                if i.get_key() == item:
                    return True
        return False
