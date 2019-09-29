def read_file(filename):
    encodings = ['utf8', 'utf16', 'cp1251']
    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print("Not valid file")
            return None
        except Exception:
            continue
    return None
