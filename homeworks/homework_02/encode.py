
def isvalid(path):
    encoding = ['utf8', 'utf16', 'cp1251']
    for enc in encoding:
        try:
            open(path, encoding=enc).read()
        except (UnicodeDecodeError, LookupError, UnicodeError):
            pass
        else:
            return enc
            break
