from time import time


class LRUCacheDecorator:

    class Entry:
        def __init__(self, inf, first_call, last_call):
            self.inf = inf
            self.first_call = first_call
            self.last_call = last_call

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}

    def __get_hash(self, arg):
        try:
            return hash(arg)
        except TypeError:
            return hash(tuple(arg))

    def __get_full_hash(self, *args, **kwargs):
        h_args = ''.join([str(self.__get_hash(arg)) for arg in args])
        h_kwargs = ''.join([str(self.__get_hash(kwargs[k])) for k in kwargs])
        return h_args + ' ' + h_kwargs

    def __call__(self, func):
        def caccess(*args, **kwargs):
            h = self.__get_full_hash(*args, **kwargs)
            if h in self.cache:
                if (self.ttl is not None and
                   (time() - self.cache[h].first_call) * 1000 > self.ttl):
                    self.cache[h].inf = func(*args, **kwargs)
                    self.cache[h].first_call = time()
                    self.cache[h].last_call = self.cache[h].first_call
                    return self.cache[h].inf
                else:
                    self.cache[h].last_call = time()
                    return self.cache[h].inf
            if len(self.cache) == self.maxsize:
                lst_of_keys = list(self.cache.keys())
                lst_of_keys = sorted(lst_of_keys, key=lambda k:
                                     self.cache[k].last_call)
                self.cache.pop(lst_of_keys[0])
            inf = func(*args, **kwargs)
            ctime = time()
            self.cache.update({h: self.Entry(inf, ctime, ctime)})
            return inf
        return caccess
