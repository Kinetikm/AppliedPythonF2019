import sys
from homeworks.homework_02.context_manager import FOpen
from homeworks.homework_02.jsonparser import jsonparse
from homeworks.homework_02.tsvparser import tsvparse
# Ваши импорты
if __name__ == '__main__':
    filename = sys.argv[1]
with FOpen(filename) as file_opened:
    if file_opened:
        last_pos = file_opened.tell()
        a = file_opened.readline()
        file_opened.seek(last_pos)
        if a[0] == '[' or a[0] == '{':
            jsonparse(file_opened)
        elif len(a.split('\t')) > 1:
            tsvparse(file_opened)
        else:
            print('Формат не валиден')
