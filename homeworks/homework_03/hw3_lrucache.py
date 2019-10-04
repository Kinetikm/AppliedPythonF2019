import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = []
        self.time_ = time.time()

    def __call__(self, func):
        def cashing(*args, **kwargs):
            if self.ttl is not None and time.time() - self.time_ > self.ttl:
                self.cache = []
            for i in range(len(self.cache)):
                if self.cache[i][0] == (args, kwargs):
                    tmp_item = self.cache[i]
                    tmp_cache = self.cache[::]
                    self.cache = tmp_cache[:i:]
                    self.cache.extend(tmp_cache[i + 1::])
                    self.cache.append(tmp_item)
                    return tmp_item[1]
            ret = func(*args, **kwargs)
            if len(self.cache) < self.maxsize:
                self.cache.append(((args, kwargs), ret))
            else:
                self.cache = self.cache[1::]
                self.cache.append(((args, kwargs), ret))
            return ret
        self.time_ = time.time()
        return cashing
