def check_codir(doc):
    for codir in ('utf8', 'utf16', 'cp1251'):
        try:
            with open(file=doc, mode='r', encoding=codir) as d:
                d = d.readline()
                return codir
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
