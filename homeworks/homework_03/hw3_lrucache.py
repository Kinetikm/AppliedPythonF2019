from time import time


class LRUCacheDecorator:
    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = {}     
        self.time = {}

    def __call__(self, func):
        def func_sur(*args, **kwargs):
            key = (args, str(kwargs), str(kwargs.values()))
            if key in self.cache:
                if self.ttl:
                    if (time() - self.time[key]) * 1000 > self.ttl:
                        self.cache.pop(key)
                        self.time.pop(key)
                        res = func(*args, **kwargs)
                        self.cache[key] = res
                        self.time[key] = time()
                        return res
                self.time[key] = time()
                return self.cache[key]
            else:
                res = func(*args, **kwargs)
                if len(self.cache) < self.maxsize:
                    self.cache[key] = res
                    self.time[key] = time()
                else:
                    oldst = max(self.time, key=lambda x: time() - self.time[x])
                    self.cache.pop(oldst)
                    self.time.pop(oldst)
                    self.cache[key] = res
                    self.time[key] = time()
                return res
        return func_sur
