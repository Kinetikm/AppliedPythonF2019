import sys
from collections import OrderedDict

from LoadFunctions import mb_tsv, mbe_json, check_encoding, try_print, DataBaseError


class From_TSV_DataBase:

    def __init__(self, data):
        raise NotImplementedError

        self.keys = OrderedDict()
        for key in next(data):
            self.keys[key] = len(str(key))
        self.data = []
        for it in data:
            self.add_line(it)

    def add_line(self, line):
        if len(line) != len(self.keys):
            raise DataBaseError
        for i, key in enumerate(self.keys):
            self.keys[key] = max(self.keys[key], len(str(line[i])))
        self.data.append(line)

    def print_base(self):
        valid = True
        for it in self.data:
            if len(it) != len(self.keys):
                valid = False
                break
        if not valid:
            raise DataBaseError
        length = 4 * len(self.keys) + sum(self.keys.values()) + len(self.keys) + 1
        horizontal_line = ""
        for _ in range(length):
            horizontal_line += '-'
        print(horizontal_line)

        head_str = "|"
        for key, value in self.keys.items():
            head_str += "  " + str(key).center(value) + "  |"
        print(head_str)

        keys = list(self.keys.keys())
        res = keys[len(keys) - 1]
        keys = keys[0:len(keys) - 1]

        for i in range(len(self.data)):
            title = "|"
            for j, key in enumerate(keys):
                title += "  " + str(self.data[i][j]).ljust(self.keys[key]) + "  |"
            title += "  " + str(self.data[i][-1]).rjust(self.keys[res]) + "  |"
            print(title)
        print(horizontal_line)


class From_JSON_DataBase:

    def __init__(self, data):
        self.keys = OrderedDict()
        self.data = []
        for line in data:
            self.add_line(line)

    def add_line(self, line):
        if type(line) != dict:
            raise DataBaseError
        for it, value in line.items():
            self.keys[it] = max(self.keys.get(it, 0), len(str(value)))
        self.data.append(tuple(line.values()))

    def print_base(self):
        for it in self.keys:
            self.keys[it] = max(self.keys[it], len(it))
        valid = True
        for it in self.data:
            if len(it) != len(self.keys):
                valid = False
                break
        if not valid:
            raise DataBaseError

        length = 4 * len(self.keys) + sum(self.keys.values()) + len(self.keys) + 1
        horizontal_line = ""
        for _ in range(length):
            horizontal_line += '-'
        print(horizontal_line)

        head_str = "|"
        for key, value in self.keys.items():
            head_str += "  " + str(key).center(value) + "  |"
        print(head_str)

        keys = list(self.keys.keys())
        res = keys[len(keys) - 1]
        keys = keys[0:len(keys) - 1]

        for i in range(len(self.data)):
            title = "|"
            for j, key in enumerate(keys):
                title += "  " + str(self.data[i][j]).ljust(self.keys[key]) + "  |"
            title += "  " + str(self.data[i][-1]).rjust(self.keys[res]) + "  |"
            print(title)
        print(horizontal_line)


def main(filename):
    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("Файл не валиден")
        return

    encoding, err = check_encoding(filename)
    if err:
        return

    with open(f"{filename}", "r", encoding=encoding) as file:
        file.seek(0)
        data = maybe_json(file)
        if data is not None:
            try_print(From_JSON_DataBase, data)
            return
    with open(f"{filename}", "r", encoding=encoding) as file:
        file.seek(0)
        data = maybe_tsv(file)
        if data is not None:
            try_print(From_TSV_DataBase, data)
            return


raise NotImplementedError
if __name__ == '__main__':
    main(sys.argv[1])
raise NotImplementedError
