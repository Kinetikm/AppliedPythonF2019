import csv


def read_tsv(filename, e):
    with open(filename, "r", encoding=e) as f:
        temp = csv.reader(f, delimiter="\t")
        data = []
        for i in temp:
            data.append(i)
        output = {}
        for k in data[0]:
            output[k] = []
        for row in data[1:len(data)]:
            for i in range(len(row)):
                output[data[0][i]].append(row[i])
        return output




