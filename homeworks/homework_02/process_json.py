import json
import sys


def process_json(filename, enc):
    try:
        file_ = open(filename, 'r', encoding=enc)
        data = json.load(file_)
        full_text = [[]]
        for key in data[0]:
            full_text[0].append(key)
        for i, dict_ in enumerate(data):
            full_text.append([])
            for key, value in dict_.items():
                full_text[i+1].append(value)
        return full_text
    except OSError:
        print('Файл не валиден')
        sys.exit()
    finally:
        file_.close()
