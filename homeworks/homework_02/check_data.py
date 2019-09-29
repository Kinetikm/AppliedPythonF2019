def encoding_check(filename):
    for enc_type in ['utf-8', 'utf-16', 'cp1251']:
        try:
            with open(filename, 'r', encoding=enc_type) as f:
                data = f.read().strip()
            return data
        except UnicodeDecodeError:
            continue
    return None
