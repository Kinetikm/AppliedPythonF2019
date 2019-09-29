def print_table(table):
    keys = [i for i in table[0].keys()]

    colmn_len = [max([len(max([key, tmp[key]], key=len)) for tmp in table])
               for key in list(table[0].keys())[:-1]]
    colmn_len.append(6)

    line = "-" * (sum(colmn_len) + 5 * len(colmn_len) + 1)

    titles = "|  " + "  |  ".join(
        j.center(m) for j, m in zip(keys, colmn_len)) + "  |"

    main_inf = ["|  " + "  |  ".join(
        tmp[j].ljust(m) for j, m in zip(keys[:3], colmn_len)) + "  |  " + str(tmp[
                    keys[-1]]).rjust(colmn_len[-1]) + "  |" for tmp in table]
    print(line)
    print(titles)
    [print(i) for i in main_inf]
    print(line)