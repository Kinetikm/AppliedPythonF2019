import os
import json
import csv
from funcs_for_fwrt import det_file_encoding, parse_json, csv_validation


def File_Writer(filename):
    if os.path.isfile(filename):
        enc = det_file_encoding(filename)
        try:
            with open(filename, 'r',
                      encoding=enc) as f:
                jsondata = json.loads(f.read())
                return parse_json(jsondata)
        except json.decoder.JSONDecodeError:
            with open(filename, 'r',
                      encoding=enc) as f:
                csvfile = csv.reader(f, delimiter="\t")
                data = []
                for line in csvfile:
                    data.append(line)
                if csv_validation(data):
                    return data
                else:
                    print('Формат не валиден')
                    return None
        except UnicodeError:
            print('Формат не валиден')
            return None
        except AttributeError:
            print('Формат не валиден')
            return None
        except IndexError:
            print('Формат не валиден')
            return None
        else:
            print('Формат не валиден')
            return None
    else:
        print('Файл не валиден')
        exit()
