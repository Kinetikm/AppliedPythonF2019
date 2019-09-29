import json
import csv


def reading(path):
    encodings = ['utf8', 'utf16', 'cp1251']
    for i in encodings:
        try:
            with open(path, 'r', encoding=i) as f:
                try:
                    data = json.loads(f.read())
                    out_list = list()
                    out_list.append(list(data[0].keys()))
                    for line in data:
                        out_list.append(list(line.values()))
                    out_list = [list(map(str, item)) for item in out_list]
                    return out_list
                except json.decoder.JSONDecodeError:
                    f.seek(0)
                    data = csv.reader(f, delimiter="\t")
                    out_list = list()
                    for line in data:
                        out_list.append(line)
                    return out_list
        except OSError:
            print('Файл не валиден')
            break
        except UnicodeError:
            pass
        except (ValueError, TypeError, SyntaxError, LookupError, EOFError):
            print('Формат не валиден')
            break
