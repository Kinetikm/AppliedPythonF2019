def detection_enc(file):
    for enc_type in ['utf-8', 'utf-16', 'windows-1251']:
        try:
            with open(file, 'r', encoding=enc_type) as f:
                f.readline()
            return enc_type
        except UnicodeError:
            continue
