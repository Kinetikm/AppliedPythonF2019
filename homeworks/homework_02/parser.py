import json
import csv


class Parser:
    def __init__(self, filename, encoding, file_format):
        self.filename = filename
        self.fencoding = encoding
        self.fformat = file_format

    def parse_data(self):
        if self.fformat == 'json':
            with open(self.filename, 'r', encoding=self.fencoding) as f:
                data = json.load(f)
                rows = []

                rows.append(list(data[0].keys()))
                for i in range(len(data)):
                    rows.append(list(data[i].values()))

                return rows

        else:
            with open(self.filename, 'r', encoding=self.fencoding) as f:
                tsvreader = csv.reader(f, delimiter="\t")
                return [line for line in tsvreader]
