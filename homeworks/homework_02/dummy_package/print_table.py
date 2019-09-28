from dummy_package import opener as op


def prt_table(file_name):
    print_table(op.json_or_tsv(file_name))


def print_table(table):
    keys = [i for i in table[0].keys()]
    max_len = [max([len(max([key, tmp[key]], key=len)) for tmp in table])
               for key in table[0].keys()]
    just_line = "-" * (sum(max_len) + 5 * len(max_len) + 1)
    titles = "|  " + "  |  ".join(
        j.center(m) for j, m in zip(keys, max_len)) + "  |"
    main_inf = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], max_len)) + "  |  " + tmp[
                    keys[-1]].rjust(max_len[-1]) + "  |" for tmp in table]
    print(just_line)
    print(titles)
    [print(i) for i in main_inf]
    print(just_line)
