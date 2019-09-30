def choose_cp1251(file):
    try:
        opened_file = open(file, encoding="cp1251")
        data = openned_file.read()
        return data
    except:
        raise None


def choose_utf8(file):
    try:
        opened_file = open(file, encoding="utf-8")
        data = openned_file.read()
        return data
    except:
        return None


def choose_utf16(file):
    try:
        opened_file = open(file, encoding="utf-16")
        data = openned_file.read()
        return data
    except:
        return None


def choose_of_encode(file):
    data = choose_utf8(file)
    if data:
        return data
    data = choose_utf16(file)
    if data:
        return data
    data = choose_cp1251(file)
    if data:
        return data
    else:
        raise
