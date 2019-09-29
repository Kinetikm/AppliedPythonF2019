def format_table(inp_lst):
    max_strs = ['']*len(inp_lst[0])
    for line in inp_lst:
        for i in range(len(inp_lst[0])):
            if len(line[i]) > len(max_strs[i]):
                max_strs[i] = line[i]

    list_of_len = list()
    for i in range(len(max_strs)):
        list_of_len.append(len(max_strs[i]))

    for i, str_ in enumerate(inp_lst[0]):
        inp_lst[0][i] = str_.center(list_of_len[i])

    for line in inp_lst[1::]:
        for i, str_ in enumerate(line[:-1:]):
            line[i] = str_.ljust(list_of_len[i])
        line[-1] = line[-1].rjust(list_of_len[-1])

    out_list = list()
    border = '-'*(sum(list_of_len) + 5*len(inp_lst[1]) + 1)
    out_list.append(border)

    for line in inp_lst:
        out_list.append('|  ' + '  |  '.join(line) + '  |')
    out_list.append(border)

    return out_list


def print_table(lst_):
    for i in range(len(lst_)):
        print(lst_[i])
