class TSVHandler:
    def _is_correct(self, tsv_text):
        self.tsv_text = tsv_text
        try:
            if type(self.tsv_text) != list or len(self.tsv_text) == 0:
                return False
            first = self.tsv_text[0]
            self.column_length = {}
            columns = first
            for key in first:
                self.column_length[key] = len(key)
            for t in self.tsv_text[1:]:
                if len(t) != len(columns):
                    return False
                for i, val in enumerate(t):
                    key = columns[i]
                    if len(str(val)) > self.column_length[key]:
                        self.column_length[key] = len(str(val))
        except:
            print(traceback.format_exc())
        return True

    def pretty_print(self, tsv_text):
        self.is_tsv = self._is_correct(tsv_text)
        if not self.is_tsv:
            print('Формат не валиден')
            return
        sep = '|'
        sep_len = sum(self.column_length.values()) + len(self.column_length.values()) * 5 + 1
        print('-' * sep_len)
        columns = self.tsv_text[0]
        for column in columns:
            print(sep + column.center(self.column_length[column] + 4), end='')
        for t in self.tsv_text[1:]:
            print(sep)
            for i, column in enumerate(t):
                escape_num = self.column_length[columns[i]] - len(str(column))
                try:
                    float(column)
                    print(sep + ' ' * (2 + escape_num) + str(column) + ' ' * 2, end='')
                except ValueError:
                    print(sep + ' ' * 2 + str(column) + ' ' * (escape_num + 2), end='')
        print(sep)
        print('-' * sep_len, end='')
