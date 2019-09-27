ENCODINGS = ['utf-8', 'utf-16', 'windows-1251']


def get_encoding(filename) -> str:
    for enc in ENCODINGS:
        try:
            with open(filename, 'r', encoding=enc) as f:
                f.readline()
            return enc
        except UnicodeError:
            continue
