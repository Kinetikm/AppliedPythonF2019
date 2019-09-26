def detect_encoding(filename):
    with open(filename, 'rb') as file:
        data = file.read()
        try:
            data.decode("UTF-8")
            return "UTF-8"
        except UnicodeDecodeError:
            return "cp1251"
