def check_encode(filename):
    for encode in ('utf8', 'utf16', 'cp1251'):
        try:
            with open(file=filename, mode='r', encoding=encode) as f:
                f = f.readline()
                return encode
        except:
            continue
        raise UnicodeDecodeError
