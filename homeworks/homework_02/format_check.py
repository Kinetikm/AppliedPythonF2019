def checker(filename):
    encoding = [
        'utf-8',
        'utf-16',
        'cp1251'
    ]

    correct_encoding = ''

    for enc in encoding:
        try:
            open(filename, encoding=enc).read()
        except (UnicodeDecodeError, LookupError, UnicodeError):
            pass
        except FileNotFoundError:
            assert "Файл не валиден"
            return None
        else:
            correct_encoding = enc
            break

    return correct_encoding
