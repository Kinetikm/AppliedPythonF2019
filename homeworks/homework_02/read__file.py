def check_codir(doc):
    for encoding_fom in ('utf8', 'utf16', 'cp1251'):
        try:
            with open(file=doc, mode='r', encoding=encoding_fom) as document:
                d = document.readline()
                return encoding_fom
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
