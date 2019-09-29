def encode_check(filename: str)->str:
    encodings = ['utf-8', 'utf-16', 'windows-1251']
    for encode in encodings:
        try:
            open(filename, encoding=encode).read()
        except (UnicodeDecodeError, LookupError, UnicodeError):
            pass
        else:
            return encode
