class GoodTable:

    def __init__(self, data: list):
        self.data = data

    def print_table(self):
        self.max_length, self.max_columns = self.calc_max_length()
        print('-' * self.max_length)
        for j, item in enumerate(self.data):
            print('|', end='')
            for i, element in enumerate(item):
                if j == 0:
                    print('  {:^{}}  '.format(element, self.max_columns[i]), end='|')
                else:
                    print('  {:<{}}  '.format(element, self.max_columns[i]), end='|')
            print('')
        print('-' * self.max_length)

    def calc_max_length(self):
        max_col = []
        for i in range(len(self.data[0])):
            max_col.append(max([len(str(item[i])) for item in self.data]))
        max_len = sum(max_col) + len(self.data[0]) * 4 + 5
        return max_len, max_col
