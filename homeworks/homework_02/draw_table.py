def get_max_columns_lens(data: list) -> list:
    """[INPUT]: [[title1, title2, ...], [row1_1,row1_2,..],..,[rown_1,rown_2,..]]
       [RETURN]: [max(len(title1), len(title2),..), max(len(row1_1), len(row2_2), ...), ...]
    """
    max_columns_lens = []
    for col in range(0, len(data[0])):
        column = []
        for row in range(0, len(data)):
            column.append(data[row][col])

        max_column_len = len(max(column, key=lambda x: len(x)))
        max_columns_lens.append(max_column_len)
    return max_columns_lens


def get_table(data: list) -> str:
    """[INPUT]: [[title1, title2, ...], [row1_1,row1_2,..],..,[rown_1,rown_2,..]]
       [RETURN]: -------------------------------
                 |  title1  |  title2  |  ...  |
                 |  row1_1  |  row1_2  |  ...  |
                 ...
                 -------------------------------
    """
    num_of_columns = len(data[0])
    max_columns_lens = get_max_columns_lens(data)

    # border_size = sum for len(max_word_in_each_row) + 2_spaces_on_every_side_of_a_word + num_of_"|"
    border_size = sum(max_columns_lens) + 4 * num_of_columns + num_of_columns + 1
    up_down_border = '-' * border_size

    table = up_down_border + '\n'
    for j, row in enumerate(data):
        rowstring = ""
        for i, column_word in enumerate(row):
                # if is a TITLE
            if j == 0:
                rowstring += "|  {:^{}}  ".format(column_word, max_columns_lens[i])
                # if last column
            elif i == len(data[0]) - 1:
                rowstring += "|  {:>{}}  ".format(column_word, max_columns_lens[i])
            else:
                rowstring += "|  {:<{}}  ".format(column_word, max_columns_lens[i])

        rowstring += '|\n'
        table += rowstring
        if j == len(data) - 1:
            table += up_down_border

    return table
