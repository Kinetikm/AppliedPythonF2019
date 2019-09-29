import chardet


def enc(filename):
    with open(filename, "rb") as f:
        temp = chardet.detect(f.readline())
        if temp['encoding'] in ['utf-8', 'utf-16', 'windows-1251', 'ascii']:
            return temp['encoding']
        else:
            return None
