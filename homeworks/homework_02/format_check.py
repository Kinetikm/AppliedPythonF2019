def checker(filename):
    encoding = [
        'utf-8',
        'utf-16',
        'cp1251'
    ]

    correct_encoding = ''

    for enc in encoding:
        try:
            file = open(filename, 'r', encoding=enc)
        except (UnicodeDecodeError, LookupError, UnicodeError):
            pass
        except FileNotFoundError:
            assert "Файл не валиден"
            return None
        else:
            correct_encoding = enc
            break
        finally:
            file.close()

    return correct_encoding
