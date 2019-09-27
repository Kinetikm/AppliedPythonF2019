import sys
import json
import os
import traceback


class JSONHandler:
    def __init__(self, json_text):
        self.json_text = json_text
        self.is_json = self._is_json()

    def _is_json(self):
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

    def pretty_print(self):
        if not self.is_json:
            return
        sep = '|'
        sep_len = sum(self.column_length.values()) + len(self.column_length.values()) * 5 + 1
        print('-' * sep_len)
        columns = list(self.column_length.keys())
        for column in columns:
            print(sep + column.center(self.column_length[column] + 4), end='')
        print(sep)
        for d in self.json_text:
            for column in columns:
                if isinstance(d[column], float) or isinstance(d[column], int):
                    print(sep + ' ' * (2 + self.column_length[column] - len(str(d[column]))) + str(d[column]) + ' ' * 2)
                else:
                    print(sep + ' ' * 2 + str(d[column]) + ' ' * (self.column_length[column] - len(str(d[column])) + 2))
        print('-' * sep_len)


class TSVHandler:
    def __init__(self, tsv_text):
        self.tsv_text = tsv_text
        self.is_tsv = self._is_tsv()

    def _is_tsv(self):
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

    def pretty_print(self):
        if not self.is_tsv:
            print('Формат не валиден')
            return
        sep = '|'
        sep_len = sum(self.column_length.values()) + len(self.column_length.values()) * 5 + 1
        print('-' * sep_len)
        columns = self.tsv_text[0]
        for column in columns:
            print(sep + column.center(self.column_length[column] + 4), end='')
        print(sep)
        for t in self.tsv_text[1:]:
            for i, column in enumerate(t):
                try:
                    float(column)
                    print(sep + ' ' * (2 + self.column_length[columns[i]] - len(str(column))) + str(column) + ' ' * 2)
                except ValueError:
                    print(sep + ' ' * 2 + str(column) + ' ' * (self.column_length[columns[i]] - len(str(column)) + 2))
        print('-' * sep_len)

if __name__ == '__main__':
    filename = sys.argv[1]
    encoding = os.path.splitext(filename)[0].split('-')[-1]
    try:
        with open(filename, encoding=encoding) as f:
            struct = json.load(f)
        json_handler = JSONHandler(struct)
        json_handler.pretty_print()
    except json.decoder.JSONDecodeError:
        try:
            with open(filename, encoding=encoding) as f:
                struct = [line.strip().split('\t') for line in f]
            tsv_handler = TSVHandler(struct)
            tsv_handler.pretty_print()
        except:
            print(traceback.format_exc())
    except FileNotFoundError:
        print('Файл не валиден')
