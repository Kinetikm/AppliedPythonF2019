from read_json import *
from enc import *


def read_file(filename):
    en = enc(filename)
    if en == "ascii":
        try:
            return read_json(filename, "utf8")
        except json.decoder.JSONDecodeError:
            return read_tsv(filename, "utf8")
        except UnicodeDecodeError:
            try:
                return read_json(filename, "cp1251")
            except json.decoder.JSONDecodeError:
                return read_tsv(filename, "cp1251")
    elif en is not None:
        try:
            return read_json(filename, en)
        except json.decoder.JSONDecodeError:
            return read_tsv(filename, en)
        except:
            print("Файл не валиден")
    else:
        print("Формат не валиден")
