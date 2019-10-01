import csv
import json
def unpack(file_path, coding) -> list:
    with open(file=file_path, mode="r", encoding=coding) as fp:
        file_ex = file_path[file_path.index('.') + 1::]
        if file_ex == 'json':
            d = json.load(fp)
            list_of_lines = [[]]
            for i in d[0].keys():
                list_of_lines[0].append(i)
            for i in range(0, len(d)):
                list_of_lines.append([])
                for j in d[i].values():
                    list_of_lines[i + 1].append(str(j))
        elif file_ex == 'tsv':
            reader = csv.reader(fp, delimiter='\t')
            list_of_lines = []
            for line in reader:
                list_of_lines.append(line)
    return list_of_lines
