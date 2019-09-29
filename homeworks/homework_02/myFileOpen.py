
def fopen(filename):
    encodings = ['utf-8', 'utf-16', 'cp1251']
    file = None
    raw = None

    for encode in encodings:
        try:
            fd = open(filename, encoding=encode)
            raw = fd.read()
            fd.close()
            return raw, 0
        except UnicodeError:
            if file:
                file.close()
                file = None
        except FileNotFoundError:
            return None, 1

    if raw is None:
        return None, 2
