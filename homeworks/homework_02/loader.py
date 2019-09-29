import json


class Loader:
    def __init__(self, filename):
        self.filename = filename
        self.fencoding = self.check_encoding()
        self.fformat = self.check_format()

    def check_format(self):
        with open(self.filename, 'r', encoding=self.fencoding) as f:
            try:
                json.load(f)
            except json.decoder.JSONDecodeError:
                return 'tsv'
            else:
                return 'json'

    def check_encoding(self):
        for encoding in ('utf-8', 'utf-16', 'cp1251'):
            try:
                with open(self.filename, 'r', encoding=encoding) as f:
                    f.readline()
            except UnicodeError:
                pass
            else:
                return encoding
