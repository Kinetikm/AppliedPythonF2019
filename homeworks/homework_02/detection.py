import chardet


def detection(file):
    with open(file, 'rb') as f:
        enc_type = chardet.detect(f.readline())['encoding']
        if enc_type in ['utf-8', 'utf-16', 'windows-1251']:
            return enc_type
        return None
