def print_view(data: list):
    column_width = [len(i) for i in data[0]]
    for item in data[1:]:
        for i in range(len(column_width)):
            if len(str(item[i])) > column_width[i]:
                column_width[i] = len(str(item[i]))

    # расчет длинны всей таблицы
    table_width = len("|") + len("  |  ") * len(column_width) + sum(column_width)

    # шаблоны для таблицы
    str_template_data = "|"
    str_template_header = "|"
    for i in range(len(column_width) - 1):
        str_template_header += "  {0[%d]:^%d}  |" % (i, column_width[i])
        str_template_data += "  {0[%d]:<%d}  |" % (i, column_width[i])
    str_template_header += "  {0[%d]:^%d}  |" % (len(column_width) - 1, column_width[len(column_width) - 1])
    str_template_data += "  {0[%d]:>%d}  |" % (len(column_width) - 1, column_width[len(column_width) - 1])

    # форматированный вывод
    print('-' * table_width)
    print(str_template_header.format(data[0]))
    for item in data[1:]:
        print(str_template_data.format(item))
    print('-' * table_width)
