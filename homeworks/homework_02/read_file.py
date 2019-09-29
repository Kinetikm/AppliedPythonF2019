def read_utf8(file_name):
    try:
        with open(file_name, encoding="utf-8") as f:
            file = f.read()
            return file
    except:
        return None


def read_utf16(file_name):
    try:
        with open(file_name, encoding="utf-16") as f:
            file = f.read()
            return file
    except:
        return None


def read_cp1251(file_name):
    try:
        with open(file_name, encoding="cp1251") as f:
            file = f.read()
            return file
    except:
        return None
