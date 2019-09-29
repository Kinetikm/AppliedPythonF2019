def file_condition(filename):
    kodi = ('utf8','utf16','cp1251')
    cntFile = 0
    cntForm = 0
    for kod in kodi:
        try:
            with open(filename, 'r', encoding=kod) as file:
                f = file.read()
                return kod
        except FileNotFoundError:
            cntFile += 1
        except:
            cntForm += 1
    if cntFile > 0:
        return 'Файл не валиден'
    elif cntForm > 0:
        return 'Формат не валиден'
