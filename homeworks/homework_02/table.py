import sys
import json
import csv
from border import file_condition
from reading import readfile
from reading_file import csv_read, json_read
from beautiful_table import cool_table
# Ваши импорты

if __name__ == '__main__':
        filename = sys.argv[1]
        if file_condition(filename) == 'Файл не валиден':
            print('Файл не валиден')
        elif file_condition(filename) == 'Формат не валиден':
            print('Формат не валиден')
        else:
            if readfile(filename) == 'json':
                text = json_read(filename)
                text = cool_table(text)
                for line in text:
                    print(line)
            elif readfile(filename) == 'csv':
                text = csv_read(filename)
                text = cool_table(text)
                for line in text:
                    print(line)
