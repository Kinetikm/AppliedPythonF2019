import csv
import json
import io
from exceptions import InvalidFormat


def read_json(string):
    return json.loads(string)


def read_tsv(string):
    reader = csv.DictReader(io.StringIO(string), delimiter='\t',
                            quoting=csv.QUOTE_NONE)
    output = []
    for i in reader:
        output.append(i)
    return output


class FormatReader:
    def __init__(self, line):
        self.keys = [
            "Название",
            "Ссылка",
            "Теги",
            "Оценка"
        ]
        self.to_dict(line)
        self.validate()

    def to_dict(self, line):
        for func in [read_json, read_tsv]:
            try:
                self.table = func(line)
                break
            except (csv.Error, json.JSONDecodeError):
                continue
        try:
            _ = self.table
        except AttributeError:
            raise InvalidFormat()

    def validate(self):
        for item in self.table:
            if not isinstance(item, dict):
                raise InvalidFormat()
            for key in item.keys():
                if key not in self.keys:
                    raise InvalidFormat()
