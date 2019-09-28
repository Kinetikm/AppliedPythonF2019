def raw_text(filename):
    encodings = ['utf8', 'utf16', 'cp1251']
    for cod in encodings:
        try:
            with open(filename, 'r', encoding=cod) as file:
                text = file.read().strip()
            return text
        except Exception:
            continue
    return None
