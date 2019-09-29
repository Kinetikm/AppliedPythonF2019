encodes = ['utf-8', 'utf-16', 'cp1251']


def encode_file(filename):
    for encode in encodes:
        try:
            with open(filename, encoding=encode) as file:
                return file.read()
        except UnicodeError:
            pass
        except FileNotFoundError:
            print('Файл не валиден')
            break
        except OSError:
            print('Формат не валиден')
            break
    return None
