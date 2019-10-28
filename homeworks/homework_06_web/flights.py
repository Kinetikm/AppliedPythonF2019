class Flights():
    def __init__(self):
        self.dct = []
        self.dct_id = []

    def get(self, get_filter=None):
        if get_filter is None:
            return sorted(self.dct, key=lambda x: x['id'])
        else:
            ret_dct = []
            for item in self.dct:
                check = True
                for key in item.keys():
                    if get_filter.get(key) is not None:
                        check = (get_filter.get(key) == item.get(key))
                if check:
                    ret_dct.append(item)
            return ret_dct

    def append(self, item):  # correct data
        if item['id'] in self.dct_id:
            return 1
        else:
            self.dct.append(item)
            self.dct_id.append(item['id'])

    def pop(self, f_id):  # correct id
        if f_id in self.dct_id:
            return self.dct.pop(self.dct_id.index(f_id))
        else:
            return 1

    def update(self, item):  # correct item
        f_id = item.get('id')
        if f_id in self.dct_id:
            cur_item = self.dct[self.dct_id.index(f_id)]
            for key in item.keys():
                cur_item[key] = item.get(key)
        else:
            return 1
