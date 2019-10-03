def ch_cp1251(file):
    try:
        with open(file, encoding='cp1251') as val:
            data = val.read()
        return data
    except UnicodeDecodeError:
        return False


def ch_utf8(file):
    try:
        with open(file, encoding='utf-8') as val:
            data = val.read()
        return data
    except(UnicodeDecodeError, UnicodeError):
        return False


def ch_utf16(file):
    try:
        with open(file, encoding='utf-16') as val:
            data = val.read()
        return data
    except:
        return False


def ch(file):
    value = ch_cp1251(file)
    if value:
        return value
    value = ch_utf16(file)
    if value:
        return value
    value = ch_utf8(file)
    if value:
        return value
    if not value:
        raise UnicodeDecodeError
