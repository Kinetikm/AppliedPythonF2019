def open_file(filename):
    code = ['utf-16', 'utf-8', 'cp1251']

    for i in code:
        try:
            with open(file=filename, encoding=i) as f:
                data = f.readlines()
                return data
        except (TypeError,  SyntaxError, AttributeError, UnicodeDecodeError, UnicodeError):
            continue
        except FileNotFoundError:
            print("Файл не валиден")
            return -1

    print("Формат не валиден")
    return -1
