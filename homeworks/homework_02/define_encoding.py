import chardet


def define_encoding(filename):
    try:
        with open(filename, 'rb') as file_:
            enc = chardet.detect(file_.read(50))
        return enc['encoding']
    except OSError:
        print('Файл не валиден')
        sys.exit()
