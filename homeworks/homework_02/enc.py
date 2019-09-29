import chardet


def enc(filename):
    with open(filename, "rb") as f:
        temp = chardet.detect(f.readline())
        if temp['encoding'] == 'utf-8' or temp['encoding'] == 'utf-16' or temp['encoding'] == 'windows-1251' or temp['encoding'] == 'ascii':
            return temp['encoding']
        else:
            return None
