import time


class LRUCacheDecorator:

    def __init__(self, maxsize, ttl):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = list()
        self.time_list = list()

    def __call__(self, func):
        def cashing(*args, **kwargs):
            for i in range(len(self.cache)):
                if self.cache[i][0] == (args, kwargs):
                    if self.ttl and (time.time() - self.time_list[i]) * 1000 > self.ttl:
                        tmp_cache = self.cache[::]
                        self.cache = tmp_cache[:i:]
                        self.cache.extend(tmp_cache[i + 1::])

                    elif self.ttl and (time.time() - self.time_list[i]) * 1000 < self.ttl:
                        tmp_item = self.cache[i]
                        tmp_cache = self.cache[::]
                        self.cache = tmp_cache[:i:]
                        self.cache.extend(tmp_cache[i + 1::])
                        self.cache.append(tmp_item)

                        tmp_cache = self.time_list[::]
                        self.time_list = tmp_cache[:i:]
                        self.time_list.extend(tmp_cache[i + 1::])
                        self.time_list.append(time.time())
                        return tmp_item[1]
                    else:
                        tmp_item = self.cache[i]
                        tmp_cache = self.cache[::]
                        self.cache = tmp_cache[:i:]
                        self.cache.extend(tmp_cache[i + 1::])
                        self.cache.append(tmp_item)
                        return tmp_item[1]

            ret = func(*args, **kwargs)
            if len(self.cache) < self.maxsize:
                self.cache.append(((args, kwargs), ret))
                if self.ttl:
                    self.time_list.append(time.time())

            else:
                self.cache = self.cache[1::]
                self.cache.append(((args, kwargs), ret))
                if self.ttl:
                    self.time_list = self.time_list[1::]
                    self.time_list.append(time.time())
            return ret
        return cashing
