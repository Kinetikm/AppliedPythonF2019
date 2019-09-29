def make_table(data: list) -> str:
    num_of_columns = len(data[0])
    max_columns_lens = []
    for col in range(len(data[0])):
        column = []
        for row in range(len(data)):
            column.append(data[row][col])

        max_column_len = len(max(column, key=lambda x: len(x)))
        max_columns_lens.append(max_column_len)

    border_size = sum(max_columns_lens) + 5 * num_of_columns + 1
    top_lower_border = '-' * border_size

    table = top_lower_border + '\n'

    for j, row in enumerate(data):
        row_string = ""
        for i, column_word in enumerate(row):
            if j == 0:                      # title в центре
                row_string += "|  {:^{}}  ".format(column_word, max_columns_lens[i])
            elif i == len(data[0]) - 1:     # оценка справа
                row_string += "|  {:>{}}  ".format(column_word, max_columns_lens[i])
            else:                           # остальное слева
                row_string += "|  {:<{}}  ".format(column_word, max_columns_lens[i])
        row_string += '|\n'
        table += row_string
        if j == len(data) - 1:
            table += top_lower_border

    return table
