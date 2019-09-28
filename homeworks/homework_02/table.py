import sys
from prTable import TablePrint
from tryjson import from_json
from trytsv import from_tsv


if __name__ == '__main__':
    file = sys.argv[1]
    done_files = []
    for code in ['utf8', 'utf16', 'cp1251']:
        if file not in done_files:
            data = from_json(file, code)
            if data is not None and len(data):
                done_files.append(file)
                TablePrint(data)
        if file not in done_files:
            data = from_tsv(file, code)
            if data is not None and len(data):
                done_files.append(file)
                TablePrint(data)
