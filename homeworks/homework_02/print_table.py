def pretty_print_table(data):
    if data[0] == "json":
        js = data[1]
        keys = js[0].keys()
        text = ["\t".join(keys)]

        for record in js:
            line = []
            for key in keys:
                line.append(str(record[key]))

            text.append("\t".join(line))
    if data[0] == "csv":
        text = data[1][:-1]

    # подсчитываем максимальную длину каждого столбца
    max_col_len = {i: 0 for i in range(len(text[0].split('\t')))}
    for line in text:
        line_data = line.split('\t')
        if not line_data:
            raise

        for col, dt in enumerate(line_data):
            if not len(dt):
                raise
            if max_col_len[col] < len(dt):
                max_col_len[col] = len(dt)

    # суммарная длина текста в столбцах + пробелы и |
    sum_len = sum(list(max_col_len.values())) + 5 * len(max_col_len) + 1
    first_line = '-' * sum_len

    for i, line in enumerate(text):
        format_line = line.split('\t')
        if len(format_line) != len(max_col_len):
            raise
        sim = '^' if i == 0 else '<'

        for j, coll in enumerate(format_line):
            sim = '>' if j == 3 else sim
            format_line[j] = ("{:" + sim + str(max_col_len[j]) + "}").format(coll)
        text[i] = format_line

    result_text = first_line + '\n'
    for line in text:
        column_line = "|  {}  |\n".format("  |  ".join(line))
        result_text += column_line
    result_text += first_line + '\n'
    print(result_text)
