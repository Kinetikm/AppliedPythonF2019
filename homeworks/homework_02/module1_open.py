def open_file(filename):
    code = ['utf-8', 'utf-16', 'cp1251']

    for i in code:
        try:
            with open(file=filename, encoding=i) as f:
                data = f.read()
                return data
        except FileNotFoundError:
            print("Файл не валиден")
            return -1
        except UnicodeDecodeError:
            continue
        except UnicodeError:
            continue
        except (TypeError, UnicodeError, SyntaxError, AttributeError):
            print("Формат не валиден")
    return -1
