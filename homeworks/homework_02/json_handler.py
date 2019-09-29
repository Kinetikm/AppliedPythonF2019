class JSONHandler:
    def _is_correct(self, json_text):
        self.json_text = json_text
        try:
            if type(self.json_text) != list or len(self.json_text) == 0:
                return False
            is_dicts = all(map(lambda x: type(x) == dict, self.json_text))
            if not is_dicts:
                return False
            first = self.json_text[0]
            self.column_length = {}
            columns = set(first.keys())
            for key in first:
                self.column_length[key] = len(key)
                cur_len = len(str(first[key]))
                if cur_len > self.column_length[key]:
                    self.column_length[key] = cur_len
            for d in self.json_text[1:]:
                if columns ^ set(d.keys()) != set():
                    return False
                for key in d.keys():
                    if len(str(d[key])) > self.column_length[key]:
                        self.column_length[key] = len(str(d[key]))
        except:
            print(traceback.format_exc())
        return True

    def pretty_print(self, json_text):
        self.is_json = self._is_correct(json_text)
        if not self.is_json:
            return
        sep = '|'
        sep_len = sum(self.column_length.values()) + len(self.column_length.values()) * 5 + 1
        print('-' * sep_len)
        columns = list(self.column_length.keys())
        for column in columns:
            print(sep + column.center(self.column_length[column] + 4), end='')
        for d in self.json_text:
            print(sep)
            for column in columns:
                escape_num = self.column_length[column] - len(str(d[column]))
                if isinstance(d[column], float) or isinstance(d[column], int):
                    print(sep + ' ' * (2 + escape_num) + str(d[column]) + ' ' * 2, end='')
                else:
                    print(sep + ' ' * 2 + str(d[column]) + ' ' * (escape_num + 2), end='')
        print(sep)
        print('-' * sep_len, end='')
