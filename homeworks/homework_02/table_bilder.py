import json
from column import column_lenght
from read_file import check_codir
from list_of_lists import csv_list_of_lists, json_to_list


def table_bilder(path):
    cod = check_codir(path)
    if cod == "Формат не валиден" or cod == "Файл не валиден":
        return cod
    with open(file=path, mode="r", encoding=cod) as f:
        try:
            data = json_to_list(json.load(f))
        except Exception:
            data = csv_list_of_lists(path, cod)
    column_count = max(len(line) for line in data)
    for line in data:
        if len(line) != column_count:
            return "Формат не валиден"
    sizes = column_lenght(data)
    tire = '-' * (sum(sizes) + 4 * len(sizes) + 5)
    print(tire)
    for i, line in enumerate(data):
        if i == 0:
            for j in range(len(data[0])):
                print("|", end="")
                print('{0:^{1}}'.format(line[j], sizes[j] + 4), end="")
            print("|", end="")
            print("\n", end="")
        else:
            for j in range(len(data[0])):
                if j == len(data[0]) - 1:
                    print("|", end="")
                    print('{0:>{1}}'.format(line[j], sizes[j] + 2), end="  |")
                else:
                    print("|  ", end="")
                    print('{0:<{1}}'.format(line[j], sizes[j]), end="  ")
            if j != len(data[0]) - 1:
                print("\n")
            else:
                print("\n", end="")
    print(tire)
