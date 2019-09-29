import os.path


def file_read(filename):
    if not os.path.exists(filename):
        return 1, None
    encodings = ['utf-8', 'utf-16', 'cp-1251']
    file = None
    data = None
    for encode in encodings:
        try:
            file = open(filename, encoding=encode)
            data = file.read()
            file.close()
            break
        except (FileNotFoundError, FileExistsError):
            return 1, None
        except UnicodeError:
            if file:
                file.close()
                file = None
    if data is None:
        return 2, None
    return 0, data
