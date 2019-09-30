import tsv
from table_parser.table_parser import TableParser


class TSVTableParseError(ValueError):
    def __init__(self, msg):
        super().__init__(msg)


class TSVTableParser(TableParser):
    def parse(self):
        if self.text == '':
            raise TSVTableParseError('No file content')
        data = [line.split('\t') for line in self.text.split('\n')]

        columns = data[0]
        values = data[1:]
        for table_entry in values:
            if len(table_entry) != len(columns):
                msg = 'Invalid number of columns: {}'.format(table_entry)
                raise TSVTableParseError(msg)
        return columns, values
