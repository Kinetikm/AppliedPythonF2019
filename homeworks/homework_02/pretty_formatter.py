from collections import defaultdict


class PrettyFormatter:
    def __init__(self, table, encoding):
        self.maxes = defaultdict(int)
        self.table = table
        self.encoding = encoding
        for item in table:
            for key in item.keys():
                length = len(str(item[key]))
                if length > self.maxes[key]:
                    self.maxes[key] = length
                if len(key) > self.maxes[key]:
                    self.maxes[key] = len(key)
        for item in self.maxes:
            self.maxes[item] += 2

    def single_item__pretty(self, item):
        inner_line = ""
        for key in item.keys():
            num_spaces = self.maxes[key] - len(str(item[key]))
            num_spaces_left = num_spaces // 2
            num_spaces_right = num_spaces - num_spaces_left
            inner_line += " " * num_spaces_left + str(item[key]) +\
                          " " * num_spaces_right + "|"
        line = f"|{inner_line}"
        return line

    def print_header(self):
        inner_line = ""
        for key in self.maxes.keys():
            num_spaces = self.maxes[key] - len(key)
            num_spaces_left = num_spaces // 2
            num_spaces_right = num_spaces - num_spaces_left
            inner_line += " " * num_spaces_left + str(key) +\
                          " " * num_spaces_right + "|"
        line = f"|{inner_line}"
        return line

    def print_whole(self):
        print(('-' * (sum(self.maxes.values()) + len(self.maxes) + 1)))
        print(self.print_header())
        for item in self.table:
            print(self.single_item__pretty(item))
        print(('-' * (sum(self.maxes.values()) + len(self.maxes) + 1)))
