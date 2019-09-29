def check_encode(filename):
    for encode in ('utf8', 'utf16', 'cp1251'):
        try:
            with open(file=filename, mode='r', encoding=encode) as f:
                f = f.readline()
                return encode
        except UnicodeError:
            pass
        except FileNotFoundError:
            return "Файл не валиден"
        except SyntaxError:
            print('Формат не валиден')
        except AttributeError:
            print('Формат не валиден')
        except IndexError:
            print('Формат не валиден')
    return "Формат не валиден"
