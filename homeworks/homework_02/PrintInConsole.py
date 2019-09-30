def print_table(data):
    if data[0] == "json":
        text = data[1]
    if data[0] == "csv":
        text = data[1][:-1]

    width_column = {i: 0 for i in range(len(text[0].split('\t')))}
    for line in text:
        line_data = line.split('\t')
        if not line_data:
            raise

        for column, data in enumerate(line_data):
            if not len(data):
                raise
            if width_column[column] < len(data):
                width_column[column] = len(data)

    sum_range = sum(list(width_column.values())) + 5 * len(width_column) + 1
    first_line = '-' * sum_range

    for i, line in enumerate(text):
        format_line = line.split('\t')
        if len(format_line) != len(width_column):
            raise
        sim = '^' if i == 0 else '<'

        for j, coll in enumerate(format_line):
            sim = '>' if j == 3 else sim
            format_line[j] = ("{:" + sim + str(width_column[j]) + "}").format(coll)
        text[i] = format_line

    result_text = first_line + '\n'
    for line in text:
        column_line = "|  {}  |\n".format("  |  ".join(line))
        result_text += column_line
    result_text += first_line + '\n'
    print(result_text)