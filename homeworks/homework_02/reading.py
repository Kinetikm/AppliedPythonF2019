import json


def read_file(path: str()):
    codecs = ['utf-8', 'utf-16', 'cp1251']
    flag_json = False
    for encode_type in codecs:
        try:
            with open(path, 'r', encoding=encode_type) as file:
                try:
                    data = json.load(file)
                    flag_json = True
                    return data, flag_json
                except json.decoder.JSONDecodeError:
                    file.seek(0)
                    data = []
                    for line in file:
                        data.append(line[:len(line) - 1])
                    return data, flag_json
        except UnicodeError:
            pass
