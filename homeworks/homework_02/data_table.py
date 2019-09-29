class DataTable:

    def __init__(self):
        self.table = []
        self.weigth = None

    def header_to_datatable(self, header: tuple):
        if self.weigth is None:
            self.table.append(header)
            self.weigth = len(header)
        elif len(header) == self.weigth:
            self.table.insert(0, header)
        else:
            raise RuntimeError

    def row_to_datatable(self, row: tuple):
        if self.weigth is None:
            self.table.append(row)
            self.weigth = len(row)
        elif len(row) == self.weigth:
            self.table.append(row)
        else:
            raise RuntimeError

    def table_output(self):
        col_weight = []
        row_len = 0
        for i, _ in enumerate(self.table[0]):
            max_len_ceil = max([len(str(ceil[i])) for ceil in self.table])
            col_weight.append(max_len_ceil)
            row_len += max_len_ceil + 5
        row_len += 1
        header = f'|  '
        boarder = '-' * row_len
        for i, elem in enumerate(self.table[0][:len(self.table[0]) - 1]):
            header += f'{elem:^{col_weight[i]}}  |  '
        header += f'{self.table[0][-1]:^{col_weight[-1]}}  |'
        print(boarder)
        print(header)
        for line in self.table[1::]:
            row = f'|  '
            for i, elem in enumerate(row[:len(line) - 1]):
                row += f'{elem:<{col_weight[i]}}  |  '
            row += f'{line[-1]:>{col_weight[-1]}}  |'
            print(row)
        print(boarder)
