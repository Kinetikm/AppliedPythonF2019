import csv
import json
from border import file_condition
# счет чсв файла
def csv_read(file):
    with open(file, 'r', encoding=file_condition(file)) as f:
        reader = csv.reader(f, delimiter='\t')
        text = []
        for row in reader:
            text.append(row)
    return text
# счет джейсона
def json_read(file):
    with open(file, 'r', encoding=file_condition(file)) as f:
        js = json.load(f)
        text = []
        first_string = []
        for key in js[0]:
            first_string.append(key)
        text.append(first_string)
        for i in range(len(js)):
            string = []
            for j in js[i]:
                string.append(js[i][j])
            text.append(string)
    return text
