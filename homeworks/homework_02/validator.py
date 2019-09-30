def check(file_name):
    for encoding in ("utf-16", "utf8", "cp1251"):
        try:
            with open(file_name, "r", encoding=encoding) as f:
                f.readlines()
                f.close()
                return encoding
        except FileNotFoundError:
            print("Файл не валиден")
            return None
        except (UnicodeDecodeError, UnicodeError, SyntaxError, AttributeError, IndexError):
            continue
    print("Формат не валиден")
    return None
