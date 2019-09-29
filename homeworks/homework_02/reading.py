from border import file_condition
import json
import csv
# смотрим какой формат
def readfile(file):
    if any(file_condition(file) == kod for kod in ('utf8','utf16','cp1251')):
        with open(file, "r", encoding=file_condition(file)) as fileR:
            try:
                text = json.load(fileR)
                return 'json'
            except:
                return 'csv'
