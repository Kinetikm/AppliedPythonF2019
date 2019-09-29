def open_file(f):
    try:
        open(f)
        return True
    except:
        raise


encode = ['utf8', 'cp1251', 'utf16', 'ASCII']


def find_encode(f):
    for enc in encode:
        try:
            open(f, encoding=enc).read(1)
            return enc
        except:
            continue
    raise UnicodeDecodeError
