import texttable


def draw_table(data):
    table = texttable.Texttable()
    headers = data[0].keys()
    table.header(headers)
    align = ['l' for i in range(len(headers) - 1)]
    align += 'r'
    table.set_cols_align(align)
    table.set_deco(table.VLINES | table.BORDER)
    table.set_chars(['-', '|', '-', ''])
    table.set_cols_width([50, 50, 9, 9])
    for line in data:
        table.add_row(list(line.values()))
    print(table.draw())
