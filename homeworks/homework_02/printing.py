def get_full_length(data):
    return [len(max(col, key=len)) for col in data]


def pretty_print(data):
    lens = get_full_length(data)
    for i in range(len(data[0])):
        tmp = [col[i] for col in data]
        if len(tmp) == 0 or len(tmp) != len(lens):
            print("Формат не валиден")
            return None
    hyps = '-' * (sum(lens) + (len(lens) - 1) * 5 + 6)
    print(hyps)
    banner = '|  ' + '  |  '.join(column[0].center(col_len)
                                  for column, col_len in zip(data,
                                                             lens)) + '  |'
    print(banner)
    data = [data[i][1:] for i in range(len(data))]
    for i in range(len(data[0])):
        row = '|  ' + '  |  '.join(column[i].ljust(col_len)
                                   for column, col_len in zip(
            data[:-1], lens)) + '  |  ' + data[-1][i].rjust(lens[-1]) + '  |'
        print(row)
    print(hyps)
