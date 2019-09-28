import sys
import os

# Мои импорты :)
from LoadFunctions import maybe_tsv, maybe_json, check_encoding, try_print
from From_TSV_DataBase import From_TSV_DataBase
from From_JSON_DataBase import From_JSON_DataBase


def main(path):
    if os.system(f"test -f {path}"):
        print("Файл не валиден")
        return

    encoding, err = check_encoding(path)
    if err:
        return

    with open(f"{path}", "r", encoding=encoding) as file:
        """
            Считается что файл не изменил
            кодировку с момента последнего прочтения
        """
        maybe_var = [(maybe_json, From_JSON_DataBase),
                     (maybe_tsv, From_TSV_DataBase)]

        for maybe, parse_func in maybe_var:
            file.seek(0)
            data = maybe(file)
            if data is not None:
                try_print(parse_func, data)
                return

if __name__ == '__main__':
    main(sys.argv[1])
