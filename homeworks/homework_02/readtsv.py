import csv


def read(filename, coding):
    with open(filename, "rb") as file:
        num_tabs = file.readline().count(b'\t')
        for line in file:
            if line.count(b'\t') != num_tabs or line.count(b'\t') == 0:
                print("Формат не валиден")
                return
    with open(filename, "r", encoding=coding) as file:
        data = csv.DictReader(file, delimiter='\t')
        new_data = []
        try:
            for l in data:
                new_data.append(dict(l))
        except:
            print("Формат не валиден")
            return
        else:
            return new_data
