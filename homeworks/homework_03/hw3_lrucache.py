# #!/usr/bin/env python
# # coding: utf-8
import time
import collections


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        '''
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        '''
        # TODO инициализация декоратора
        # #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
        # raise NotImplementedError
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = collections.OrderedDict()

    def __call__(self, *args, **kwargs):
        self.func = args[0]

        def decoreted(*args, **kwargs):

            arg = args
            kwarg = kwargs

            size_cache = len(self.cache.keys())
            if self.ttl is not None:
                if arg in self.cache.keys() and self.cache[arg][0] == kwarg:
                    if time.time() - self.cache[arg][1] < self.ttl:
                        return self.cache[arg][2]
                    elif time.time() - self.cache[arg][1] > self.ttl and size_cache < self.maxsize:
                        self.cache.pop(arg)
                        self.cache[arg] = []
                        self.cache.move_to_end(key=arg, last=True)
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(time.time())
                        self.cache[arg].append(self.func(*args, **kwargs))
                        return self.cache[arg][2]
                    elif time.time() - self.cache[arg][1] > self.ttl and size_cache >= self.maxsize:
                        self.cache[arg] = []
                        self.cache.popitem(last=False)
                        self.cache.move_to_end(key=arg, last=True)
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(time.time())
                        self.cache[arg].append(self.func(*args, **kwargs))
                        return self.cache[arg][2]
                elif arg not in self.cache:
                    if size_cache < self.maxsize:
                        self.cache[arg] = []
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(time.time())
                        self.cache[arg].append(self.func(*args, **kwargs))

                        return self.cache[arg][2]
                    else:
                        self.cache.popitem(last=False)
                        self.cache.move_to_end(key=arg, last=True)
                        self.cache[arg] = []
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(time.time())
                        self.cache[arg].append(self.func(*args, **kwargs))
                        return self.cache[arg][2]
            else:
                if arg in self.cache and self.cache[arg][0] == kwarg:
                    return self.cache[arg][1]
                elif arg not in self.cache:

                    if size_cache < self.maxsize:
                        self.cache[arg] = []
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(self.func(*args, **kwargs))
                        return self.cache[arg][1]
                    else:
                        self.cache.popitem(last=True)
                        self.cache[arg] = []
                        self.cache.move_to_end(key=arg, last=True)
                        self.cache[arg].append(kwarg)
                        self.cache[arg].append(self.func(*args, **kwargs))

                        return self.cache[arg][1]

        return decoreted
