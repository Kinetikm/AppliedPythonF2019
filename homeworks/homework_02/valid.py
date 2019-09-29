def validen(name_of_fail):
    encoding = ['utf8', 'utf16', 'cp1251']
    for en in encoding:
        try:
            with open(name_of_fail, "r", encoding=en) as read_file:
                d = read_file.read()
                return en
        except UnicodeError:
            pass
        except FileNotFoundError:
            return 'Файл не валиден'
        except JSONDecodeError:
            return 'Формат не валиден'
    return 'Файл не валиден'
