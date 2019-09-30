import opener as op


def prt_table(file_name):
    print_table(op.json_tsv(file_name))


def print_table(table):
    keys = [key for key in table[0].keys()]
    ln = [max([len(max([key, tmp[key]], key=len)) for tmp in table]) for key in table[0].keys()]
    empty = "-" * (sum(ln) + 5 * len(ln) + 1)
    title = "|  " + "  |  ".join(i.center(k) for i, k in zip(keys, ln)) + "  |"
    gen = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], ln)) + "  |  " + tmp[
                    keys[-1]].rjust(ln[-1]) + "  |" for tmp in table]
    print(empty)
    print(title)
    for i in gen:
        print(i)
    print(empty)
