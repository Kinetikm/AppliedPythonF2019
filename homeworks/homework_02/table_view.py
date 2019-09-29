class Table:
    def __init__(self):
        self.table = list()
        self.width = None

    def add_header(self, header: tuple):
        if self.width is None:
            self.table.append(header)
            self.width = len(header)
        elif len(header) == self.width:
            self.table.insert(0, header)
        else:
            raise RuntimeError

    def add_row(self, row: tuple):
        if self.width is None:
            self.table.append(row)
            self.width = len(row)
        elif len(row) == self.width:
            self.table.append(row)
        else:
            raise RuntimeError

    def print_table(self):
        column_width = []
        line_len = 0
        for i, _ in enumerate(self.table[0]):
            max_el_width = max([len(str(p[i])) for p in self.table])
            column_width.append(max_el_width)
            line_len += max_el_width + 5
        line_len += 1
        horizontal_delimiter = '-' * line_len
        formatted_header = f'|  '
        for i, name in enumerate(self.table[0][:len(self.table[0]) - 1:]):
            formatted_header += f'{name:^{column_width[i]}}  |  '
        formatted_header += f'{self.table[0][-1]:^{column_width[-1]}}  |'
        print(horizontal_delimiter)
        print(formatted_header)
        for row in self.table[1::]:
            line = f'|  '
            for i, item in enumerate(row[:len(row) - 1:]):
                line += f'{item:<{column_width[i]}}  |  '
            line += f'{row[-1]:>{column_width[-1]}}  |'
            print(line)
        print(horizontal_delimiter)
