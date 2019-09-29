class FOpen(object):

    encoding = [
        'utf-8',
        'utf-16',
        'cp1251'
    ]

    def __init__(self, file):
        self.file = file

    def __enter__(self):
        for enc in self.encoding:
            try:
                open(self.file, encoding=enc).read()
            except (UnicodeDecodeError, LookupError, UnicodeError):
                pass
            else:
                correct_encoding = enc
                break
        try:
            self.fp = open(self.file, encoding=correct_encoding)
            return self.fp
        except IOError:
            print("Файл не валиден")

    def __exit__(self, exp_type, exp_value, exp_tr):
        try:
            self.fp.close()
        except AttributeError:
            return True
