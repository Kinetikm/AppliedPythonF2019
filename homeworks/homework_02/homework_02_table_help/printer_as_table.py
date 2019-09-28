def print_data_as_table(list_data):
    col_size = {}
    for row in list_data:
        for i, col in enumerate(row):
            col_size[i] = max(col_size.get(i, 0), len(str(col)))
    ncols = len(col_size)
    result = []
    for row in list_data:
        row = list(row) + [''] * (ncols - len(row))
        for i, col in enumerate(row):
            if i == len(row) - 1:
                row[i] = str(col).rjust(col_size[i])
            else:
                row[i] = str(col).ljust(col_size[i])
        result.append(row)
    count_ = sum(map(lambda tup: tup[1], col_size.items())) + 5 * len(col_size.keys()) + 1
    print("-" * count_)
    for row in result:
        result_row = ""
        for item in row:
            result_row += "|  " + item + "  "
        result_row += "|"
        print(result_row)
    print("-" * count_)
