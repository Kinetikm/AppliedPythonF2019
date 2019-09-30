def reader(filename):
    l = []
    for coding in ('utf8', 'cp1251', 'utf16le', 'utf-16be'):
        try:
            with open(filename, encoding=coding) as f:
                for line in f:
                    l.append(line.strip())
            return l
        except UnicodeDecodeError:
            continue
