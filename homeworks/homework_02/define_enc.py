enc_list = ['utf8', 'cp1251', 'utf16', 'ASCII']


def define(file):
    for enc in enc_list:
        try:
            open(file, encoding=enc).read(1)
            return enc
        except:
            continue
    return None
