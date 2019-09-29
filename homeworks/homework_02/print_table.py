
def print_table(text):
    max_len = {i: 0 for i in range(len(text[0].split('\t')))}
    for line in text:
        line_d = line.split('\t')
        if not line_d:
            raise

        for p in range(len(line_d)):
            if not len(line_d[p]):
                raise
            if max_len[p] < len(line_d[p]):
                max_len[p] = len(line_d[p])

    sum_len = sum(list(max_len.values())) + 5 * len(max_len) + 1
    first_line = '-' * sum_len

    for i in range(len(text)):
        format_line = text[i].split('\t')
        if len(format_line) != len(max_len):
            raise
        sim = '^' if i == 0 else '<'

        for j in range(len(format_line)):
            sim = '>' if j == 3 else sim
            format_line[j] = ("{:" + sim + str(max_len[j]) + "}").format(format_line[j])
        text[i] = format_line

    result = first_line + '\n'
    for line in text:
        column_line = "|  {}  |\n".format("  |  ".join(line))
        result += column_line
    result += first_line + '\n'
    print(result)
