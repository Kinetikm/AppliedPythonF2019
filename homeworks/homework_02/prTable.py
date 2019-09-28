def TablePrint(data):
    length = {}
    for count, line in enumerate(data):
        for key, value in line.items():
            if key not in length.keys():
                if len(key) > len(str(value)):
                    length.update({key: len(key)})
                else:
                    length.update({key: len(str(value))})
            else:
                if len(str(value)) > length[key]:
                    length[key] = len(str(value))
    pattern = ''
    header_pattern = ''
    for value in length.values():
        pattern += ('|  {:' + str(value) + '}  ')
        header_pattern += ('|  {:^' + str(value) + '}  ')
    pattern += '|\n'
    header_pattern += '|\n'
    text = header_pattern.format(*length.keys())
    cor_len = len(text[:-1])
    for i in data:
        text += pattern.format(*i.values())
    print('--' * (cor_len // 2) + '-')
    print(text[:-1])
    print('--' * (cor_len // 2) + '-')
