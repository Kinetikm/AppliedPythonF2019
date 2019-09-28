def read_utf8(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            data = f.read()
            return data
    except:
        return None


def read_utf16(filename):
    try:
        with open(filename, encoding="utf-16") as f:
            data = f.read()
            return data
    except:
        return None


def read_cp1251(filename):
    try:
        with open(filename, encoding="cp1251") as f:
            data = f.read()
            return data
    except:
        raise


def read_data_from_file(filename):
    dt = read_utf8(filename)
    if not dt:
        dt = read_utf16(filename)
    if not dt:
        dt = read_cp1251(filename)
    return dt
