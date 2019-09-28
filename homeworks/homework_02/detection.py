import chardet


def detection_enc(file):
    with open(file, 'rb') as f:
        enc_type = chardet.detect(f.readline())['encoding']
        if enc_type in ['utf-8', 'utf-16', 'windows-1251']:
            return enc_type
        print('Формат не валиден')
        return None
