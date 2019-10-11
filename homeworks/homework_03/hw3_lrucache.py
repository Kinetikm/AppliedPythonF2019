from time import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        """
        :param maxsize: максимальный размер кеша
        :param ttl: время в млсек, через которое кеш
                    должен исчезнуть
        """
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}
        self.cache_time = {}

    def __call__(self, func):
        def cache(*args, **kwargs):
            cache_key = hash(str(args) + str(kwargs))

            if cache_key not in self.cache:
                res = func(*args, **kwargs)
                self.cache[cache_key] = res
                self.cache_time[cache_key] = time()
            else:
                if self.ttl and (time() - self.cache_time[cache_key]) * 1000 > self.ttl:
                    res = func(*args, **kwargs)
                    self.cache_time[cache_key] = time()
                    self.cache[cache_key] = res
                else:
                    self.cache_time[cache_key] = time()
                    res = self.cache[cache_key]

            self.update_cache()

            return res

        return cache

    def update_cache(self):
        if len(self.cache) > self.maxsize:
            oldest_key = list(self.cache_time.keys())[list(self.cache_time.values()).index(min(self.cache_time.values()))]
            del self.cache[oldest_key]
            del self.cache_time[oldest_key]