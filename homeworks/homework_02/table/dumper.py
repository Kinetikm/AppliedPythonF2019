
def dump_table(table: list):

    t_header = table.pop(0)

    max_widths = dict()
    for col in t_header:
        max_widths[col] = len(col)

    # определяем максимальную ширину колонок
    for row in table:
        for (i, col) in enumerate(t_header):
            max_widths[col] = max(max_widths[col], len(str(row[i])))

    table_width = len(t_header) * 5 + 1 + sum(max_widths.values())
    # print("table max length:", table_width)

    table_boarder = '-' * table_width
    # начало таблицы
    print(table_boarder)

    # шаблон для тела заголовка талбицы
    header_tmpl = [('{:^' + '{}'.format(max_widths[col]) + '}') for col in t_header]
    header_tmpl = '  |  '.join(header_tmpl)
    header_tmpl = '|  {}  |'.format(header_tmpl)

    # заголовок
    print(header_tmpl.format(*t_header))

    # шаблон для тела таблицы
    body_tmpl = [('{:' + '{}'.format(max_widths[col]) + '}') for col in t_header]
    body_tmpl = '  |  '.join(body_tmpl)
    body_tmpl = '|  {}  |'.format(body_tmpl)

    # тело таблицы
    for row in table:
        print(body_tmpl.format(*row))

    # конец таблицы
    print(table_boarder)

    return
