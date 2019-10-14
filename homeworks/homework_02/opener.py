import json

import format_check as format_check


def opener(filename):
    """Открываем, проверяем на ошибки и выдаём текст, формат файла"""

    encoding_file = format_check.checker(filename)
    if encoding_file is not None:
        my_file = open(filename, 'r', encoding=encoding_file)

        try:
            # применяю такой странный подход, так как при нормальном открывании через load почему-то ломается.
            data_file = json.loads(my_file.read())
            return data_file, "json"

        except json.decoder.JSONDecodeError:
            my_file = open(filename, 'r', encoding=encoding_file)
            data = [line.strip().split('\t') for line in my_file]
            return data, "tsv"
        except:
            print("Формат не валиден")
            return None, None
        finally:
            my_file.close()
    else:
        print("Файл не валиден")
        return None, None
