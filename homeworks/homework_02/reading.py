import json
import csv


DEFAULT_ENCODINGS = ['utf-16', 'utf8', 'cp1251']


def define_encoding(filename, enclist=DEFAULT_ENCODINGS):
    for enc in enclist:
        try:
            with open(filename, 'r', encoding=enc) as f:
                # Костыль
                f.readline()
                return enc
        except UnicodeDecodeError:
            continue
        except UnicodeError:
            continue
        except FileNotFoundError:
            return -1
    return None


def read_file(filename):
    enc = define_encoding(filename)
    if not enc:
        print("Формат не валиден")
        return None
    elif enc == -1:
        print("Файл не валиден")
        return None
    try:
        return read_json(filename, enc)
    except UnicodeDecodeError:
        return read_tsv(filename, enc)


def read_tsv(filename, enc):
    with open(filename, 'r', encoding=enc) as tsv:
        head = tsv.readline()
        headers = head.strip().split('\t')
        n_cols = len(headers)
        data = [[header] for header in headers]
        for line in tsv:
            tmp = line.strip().split('\t')
            for i in range(n_cols):
                data[i].append(tmp[i])
    return data


def read_json(filename, enc):
    with open(filename, 'r', encoding=enc) as f:
        raw_data = json.load(f, object_pairs_hook=dict, parse_int=str)
    head = raw_data[0]
    headers = head.keys()
    data = [[header] for header in headers]
    n_cols = len(head)
    for item in raw_data:
        for i, val in enumerate(item.values()):
            data[i].append(val)

    return data
