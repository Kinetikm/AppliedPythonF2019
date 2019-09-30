def find_column_width(text_dict, key):
    col_max = len(key)
    for i in range(len(text_dict)):
        if len(text_dict[i][key]) > col_max:
            col_max = len(text_dict[i][key])  # find max_column size
    return col_max


def find_width(text_dict):
    width = 5 * (len(text_dict[0]) - 1) + 6     # comment
    for key in text_dict[0]:
        width += find_column_width(text_dict, key)
    return width


def draw_head(text_dict):
    st = ''
    for key in text_dict[0]:
        cw = find_column_width(text_dict, key)     # column width
        st += '|  '
        st += ' ' * (cw//2 - len(key)//2)   # spaces in front of key
        st += key              # key
        st += ' ' * (cw - (cw//2 - len(key)//2) - len(key))        # spaces above key
        st += '  '
    st += '|'
    st += '\n'
    return st


def draw_body(text_dict):
    body = ''
    for i in range(len(text_dict)):
        # draw line
        line = ''
        for key in text_dict[0]:
            cw = find_column_width(text_dict, key)
            if len(key) == cw:
                line += '|  '
                line += ' ' * (cw - len(text_dict[i][key]))
                line += text_dict[i][key]
                line += '  '
            else:
                line += '|  '
                line += text_dict[i][key]
                line += ' ' * (cw - len(text_dict[i][key]))
                line += '  '
        line += '|'
        line += '\n'
        body += line
    return body


def draw_table(text_dict):
    table = '-' * find_width(text_dict) + '\n'
    table += draw_head(text_dict)
    table += draw_body(text_dict)
    table += '-' * find_width(text_dict)
    return table
