def print_data(data_list):
    col_size = {}
    for row in data_list:
        for i, col in enumerate(row):
            col_size[i] = max(col_size.get(i, 0), len(str(col)))
    n_cols = len(col_size)
    result = []
    for row in data_list:
        row = list(row) + [''] * (n_cols - len(row))
        for i, col in enumerate(row):
            if i == len(row) - 1:
                row[i] = str(col).rjust(col_size[i])  # для последнего
            else:
                row[i] = str(col).ljust(col_size[i])  # для остальных
        result.append(row)
    count = sum(col_size.values()) + 5 * len(col_size.keys()) + 1
    print("-" * count)
    for row in result:
        result_row = ""
        for item in row:
            result_row += "|  " + item + "  "
        result_row += "|"
        print(result_row)
    print("-" * count)
