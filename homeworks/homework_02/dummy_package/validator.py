import sys


def check_encode(file_name):
    for encod in ("utf-16", "utf8", "cp1251"):
        try:
            with open(file_name, "r", encoding=encod) as f:
                f.readlines()
                f.close()
                return encod
        except FileNotFoundError:
            print("Файл не валиден")
            return None
        except (UnicodeDecodeError, UnicodeError):
            continue
    print("Формат не валиден")
    return None
