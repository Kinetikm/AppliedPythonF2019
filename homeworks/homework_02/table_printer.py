def get_columns_widths(table, num_column):
    """
    determinate widths of columns by size of entries
    :param table: list with tables rows
    :param num_column: int, num columns in table
    :return: list of columns widths
    """
    data_length = [[len(str(item)) for item in line] for line in table]
    widths = [0 for _ in range(num_column)]
    for line in data_length:
        for i in range(num_column):
            if widths[i] < line[i]:
                widths[i] = line[i]
    return widths


def print_table(table, num_column):
    """
    Print pretty formed table
    :param table: list of table rows, each row list of entries
    :param num_column: int
    :return: None
    """
    num_spaces = 2
    header = table[0]
    lines = table[1:]
    columns_widths = get_columns_widths(table, num_column)
    delimeter_string = '-'*(sum(columns_widths) + num_spaces*2*num_column + num_column + 1)

    header_template = '|'
    for i in columns_widths:
        header_template += '{space}{{:^{widht}}}{space}|'.format(space=' '*num_spaces, widht=i)

    row_template = '|'
    for i in columns_widths[:len(columns_widths)-1]:
        row_template += '{space}{{:<{widht}}}{space}|'.format(space=' '*num_spaces, widht=i)
    row_template += '{space}{{:>{widht}}}{space}|'.format(space=' '*num_spaces, widht=columns_widths[-1])

    print(delimeter_string)
    print(header_template.format(*header))
    for line in lines:
        print(row_template.format(*line))
    print(delimeter_string)
