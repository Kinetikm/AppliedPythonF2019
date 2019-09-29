def open(filename):
    text = None
    file = None
    encodings = ['utf-8', 'utf-16', 'cp1251']
    for enc in encodings:
        try:
            file = open(filename, encoding=enc)
            text = file.read()
            file.close()
            break
        except (FileNotFoundError, FileExistsError):
            return 1, None
        except UnicodeError:
            if file:
                file.close()
                file = None
    if text is None:
        return 2, None
    return 0, text
