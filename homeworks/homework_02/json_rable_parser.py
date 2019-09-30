import json
from table_parser.table_parser import TableParser


class JSONTableParserFormatError(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class JSONTableParser(TableParser):
    def parse(self):
        try:
            data = json.loads(self.text)
        except Exception as e:
            raise JSONTableParserFormatError(str(e))
        if not isinstance(data, list):
            raise JSONTableParserFormatError('JSON is not a list')
        if len(data) == 0:
            raise JSONTableParserFormatError('JSON list is empty')

        columns = data[0].keys()
        column_set = set(columns)

        column_values = dict((column, []) for column in columns)

        for table_entry in data:
            entry_column_set = set(table_entry.keys())
            if entry_column_set != column_set:
                msg = 'Invalid JSON key set: {} expected but {} found'.format(
                    column_set,
                    entry_column_set
                )
                raise JSONTableParserFormatError(msg)
            for column in entry_column_set:
                column_values[column].append(table_entry[column])

        column_values = [column_values[column] for column in columns]
        values = list(zip(*column_values))

        return list(columns), values
