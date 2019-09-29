import json
from read_module import readjson, readtsv


def get_enc(filename):
    encoding = ['utf-8', 'utf-16', 'Windows-1251']
    for enc in encoding:
        try:
            open(filename, 'r', encoding=enc).read()
        except (UnicodeError, LookupError):
            pass
        else:
            return enc
    return False


def get_format(filename):
    enc = get_enc(filename)
    try:
        readjson(filename, enc)
    except (UnicodeError, json.decoder.JSONDecodeError, FileNotFoundError):
        pass
    else:
        return 'json'
    try:
        readtsv(filename, enc)
    except (UnicodeError, FileNotFoundError):
        pass
    else:
        return 'tsv'


def FileChecker(filename):
    try:
        open(filename)
    except (FileExistsError, FileNotFoundError):
        print('Файл не валиден')
        return False
    return True
