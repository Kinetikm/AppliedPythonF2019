def file_enc(filename):
    encoding = ['utf8', 'utf16', 'cp1251']
    for enc in encoding:
        try:
            with open(filename, 'r', encoding=enc) as file:
                file.read()
        except UnicodeError:
            pass
        else:
            return enc
            break
