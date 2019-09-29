def get_encoding(path) -> str:
    encodings = ['utf-8', 'utf-16', 'cp1251']
    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                f.readline()
            return enc
        except UnicodeError:
            continue
